import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import statsmodels.api as sm
from statsmodels.graphics.gofplots import qqplot

# Creating synthetic data based on the problem description
# A 2×3×2 design with 5 replications

# Set random seed for reproducibility
np.random.seed(123)

# Define factors
factor_a_levels = ['Below MWCO', 'Above MWCO']  # Molecular Size
factor_b_levels = ['log Kow < -1', '-1 < log Kow < 3', 'log Kow > 3']  # Solute Hydrophobicity
factor_c_levels = ['θ < 45°', 'θ > 45°']  # Membrane Hydrophobicity
replications = 5

# Create a dataframe to store all experimental conditions and results
data = []

# Generate synthetic rejection rate data with some expected patterns
# Higher rejection for smaller molecules (below MWCO)
# Higher rejection for more hydrophobic solutes
# Higher rejection for more hydrophobic membranes
# Include some interaction effects

for a in range(2):  # Factor A: 2 levels
    for b in range(3):  # Factor B: 3 levels
        for c in range(2):  # Factor C: 2 levels
            for rep in range(replications):
                # Base rejection rate
                rejection = 0.5
                
                # Main effects
                if a == 0:  # Below MWCO
                    rejection += 0.2  # Better rejection for smaller molecules
                
                if b == 1:  # Medium hydrophobicity
                    rejection += 0.1
                elif b == 2:  # High hydrophobicity
                    rejection += 0.15
                
                if c == 1:  # More hydrophobic membrane
                    rejection += 0.15
                
                # Two-way interactions
                if a == 0 and b == 2:  # Small molecules with high hydrophobicity
                    rejection += 0.1
                
                if b == 2 and c == 1:  # High solute hydrophobicity with hydrophobic membrane
                    rejection += 0.08
                
                # Three-way interaction
                if a == 0 and b == 2 and c == 1:
                    rejection += 0.05
                
                # Add some random noise
                rejection += np.random.normal(0, 0.05)
                
                # Ensure rejection is between 0 and 1
                rejection = max(0, min(1, rejection))
                
                data.append({
                    'A': factor_a_levels[a],
                    'B': factor_b_levels[b],
                    'C': factor_c_levels[c],
                    'Replication': rep + 1,
                    'Rejection': rejection
                })

# Create DataFrame
df = pd.DataFrame(data)

# Display the first few rows
print("Data Preview:")
print(df.head())

# Summary statistics
print("\nSummary Statistics:")
summary = df.groupby(['A', 'B', 'C'])['Rejection'].agg(['mean', 'std', 'count'])
print(summary)

# (a) Full Model Analysis
print("\n(a) Full Model with All Interactions:")
formula_full = "Rejection ~ C(A) + C(B) + C(C) + C(A):C(B) + C(A):C(C) + C(B):C(C) + C(A):C(B):C(C)"
model_full = ols(formula_full, data=df).fit()
anova_full = anova_lm(model_full, typ=2)
print(anova_full)

# Identify significant effects at alpha = 0.05
print("\nSignificant Effects at α = 0.05:")
for effect, row in anova_full.iterrows():
    if row['PR(>F)'] < 0.05:
        print(f"{effect}: p-value = {row['PR(>F)']:.5f}")

# (b) Model without Three-way Interaction
print("\n(b) Model without Three-factor Interaction:")
formula_reduced = "Rejection ~ C(A) + C(B) + C(C) + C(A):C(B) + C(A):C(C) + C(B):C(C)"
model_reduced = ols(formula_reduced, data=df).fit()
anova_reduced = anova_lm(model_reduced, typ=2)
print(anova_reduced)

# Identify significant effects at alpha = 0.05
print("\nSignificant Effects at α = 0.05 (Reduced Model):")
for effect, row in anova_reduced.iterrows():
    if row['PR(>F)'] < 0.05:
        print(f"{effect}: p-value = {row['PR(>F)']:.5f}")

# (c) Residual Analysis for Full Model
residuals_full = model_full.resid
fitted_full = model_full.fittedvalues

# Homoscedasticity test
print("\n(c) Homoscedasticity Test (Breusch-Pagan):")
bp_test = sm.stats.diagnostic.het_breuschpagan(residuals_full, model_full.model.exog)
print(f"Lagrange Multiplier statistic: {bp_test[0]:.4f}")
print(f"p-value: {bp_test[1]:.4f}")
print(f"Homoscedasticity assumption {'satisfied' if bp_test[1] > 0.05 else 'violated'}")

# Normality test
print("\nNormality Test (Shapiro-Wilk):")
w, p_value = stats.shapiro(residuals_full)
print(f"W statistic: {w:.4f}")
print(f"p-value: {p_value:.4f}")
print(f"Normality assumption {'satisfied' if p_value > 0.05 else 'violated'}")

# (d) Square root arcsin transformation
print("\n(d) Square Root Arcsin Transformation:")
# Apply transformation
df['Transformed_Rejection'] = np.arcsin(np.sqrt(df['Rejection']))

# Fit full model to transformed data
formula_transformed = "Transformed_Rejection ~ C(A) + C(B) + C(C) + C(A):C(B) + C(A):C(C) + C(B):C(C) + C(A):C(B):C(C)"
model_transformed = ols(formula_transformed, data=df).fit()
anova_transformed = anova_lm(model_transformed, typ=2)
print(anova_transformed)

# Residual analysis for transformed model
residuals_transformed = model_transformed.resid
fitted_transformed = model_transformed.fittedvalues

# Homoscedasticity test for transformed data
print("\nHomoscedasticity Test (Breusch-Pagan) for Transformed Data:")
bp_test_transformed = sm.stats.diagnostic.het_breuschpagan(residuals_transformed, model_transformed.model.exog)
print(f"Lagrange Multiplier statistic: {bp_test_transformed[0]:.4f}")
print(f"p-value: {bp_test_transformed[1]:.4f}")
print(f"Homoscedasticity assumption {'satisfied' if bp_test_transformed[1] > 0.05 else 'violated'}")

# Normality test for transformed data
print("\nNormality Test (Shapiro-Wilk) for Transformed Data:")
w_transformed, p_value_transformed = stats.shapiro(residuals_transformed)
print(f"W statistic: {w_transformed:.4f}")
print(f"p-value: {p_value_transformed:.4f}")
print(f"Normality assumption {'satisfied' if p_value_transformed > 0.05 else 'violated'}")

# Create visualizations for both original and transformed data
plt.figure(figsize=(15, 10))

# Original Data Analysis
plt.subplot(2, 2, 1)
plt.scatter(fitted_full, residuals_full)
plt.axhline(y=0, color='r', linestyle='-')
plt.xlabel('Fitted Values')
plt.ylabel('Residuals')
plt.title('Residuals vs Fitted (Original Data)')

plt.subplot(2, 2, 2)
qqplot(residuals_full, line='s', ax=plt.gca())
plt.title('Q-Q Plot (Original Data)')

# Transformed Data Analysis
plt.subplot(2, 2, 3)
plt.scatter(fitted_transformed, residuals_transformed)
plt.axhline(y=0, color='r', linestyle='-')
plt.xlabel('Fitted Values')
plt.ylabel('Residuals')
plt.title('Residuals vs Fitted (Transformed Data)')

plt.subplot(2, 2, 4)
qqplot(residuals_transformed, line='s', ax=plt.gca())
plt.title('Q-Q Plot (Transformed Data)')

plt.tight_layout()
plt.savefig('residual_analysis.png')

# Create interaction plots for significant interactions
# Example: If A*B interaction is significant
plt.figure(figsize=(10, 6))
for c_level in factor_c_levels:
    subset = df[df['C'] == c_level]
    means = subset.groupby(['A', 'B'])['Rejection'].mean().reset_index()
    
    for a_level in factor_a_levels:
        a_data = means[means['A'] == a_level]
        plt.plot(a_data['B'], a_data['Rejection'], marker='o', label=f'A={a_level}, C={c_level}')
        
plt.xlabel('Factor B (Solute Hydrophobicity)')
plt.ylabel('Mean Rejection Rate')
plt.title('Interaction Plot: Factors A, B, and C')
plt.legend()
plt.grid(True)
plt.savefig('interaction_plot.png')

print("\nAnalysis Completed. Check the figures for visual assessment.")