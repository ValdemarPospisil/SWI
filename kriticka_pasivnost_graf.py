import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Pro prostředí bez GUI

# Nastavení českých znaků
plt.rcParams['font.family'] = 'DejaVu Sans'

# Data z experimentu
models = ['Claude', 'ChatGPT', 'Gemini', 'DeepSeek']
neutral_scores = [62, 86, 85, 97]
positive_scores = [23, 75, 45, 85]
negative_scores = [84, 88, 86, 94]

# Vytvoření DataFrame pro jednodušší manipulaci
data = pd.DataFrame({
    'Model': np.repeat(models, 3),
    'Prompt': ['Neutrální', 'Pozitivní', 'Negativní'] * 4,
    'Skóre': neutral_scores + positive_scores + negative_scores
})

# Rozdíly mezi neutrálním a pozitivním promptem
prompt_differences = []
for i in range(len(models)):
    prompt_differences.append(neutral_scores[i] - positive_scores[i])

# Vytvoření hlavního grafu
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

# 1. Graf - sloupcový pro srovnání skóre podle různých promptů
df_pivot = data.pivot(index='Model', columns='Prompt', values='Skóre')
df_pivot.plot(kind='bar', ax=ax1)
ax1.set_title('Celkové skóre podle typu promptu a modelu', fontsize=12, fontweight='bold')
ax1.set_ylabel('Celkové skóre (0-100)')
ax1.set_ylim(0, 100)
ax1.grid(axis='y', linestyle='--', alpha=0.7)
ax1.legend(title='Typ promptu')

# 2. Graf - procentuální pokles při pozitivním promptu
x = np.arange(len(models))
width = 0.5
differences = np.array(prompt_differences) / np.array(neutral_scores) * 100

bars = ax2.bar(x, differences, width, color='firebrick')
ax2.set_title('Pokles výkonu při pozitivním promptu', fontsize=12, fontweight='bold')
ax2.set_xlabel('Model')
ax2.set_ylabel('Pokles skóre (%)')
ax2.set_xticks(x)
ax2.set_xticklabels(models)
ax2.grid(axis='y', linestyle='--', alpha=0.7)

# Přidání hodnot na vrchol sloupců
for i, v in enumerate(differences):
    ax2.text(i, v + 1, f'{v:.1f}%', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('llm_code_review_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

print("Graf byl úspěšně vytvořen a uložen jako 'llm_code_review_comparison.png'")
