import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use('Agg')  # Pro prostředí bez GUI

# Nastavení českých znaků
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False # Zajištění správného zobrazení znaménka mínus

# Data z experimentu
models = ['Claude', 'ChatGPT', 'Gemini', 'DeepSeek']
prompt_types = ['Neutrální', 'Pozitivní', 'Negativní']

neutral_scores = [54, 74, 74, 89]
positive_scores = [17, 63, 43, 73]
negative_scores = [73, 79, 80, 84]

# Správné sestavení dat pro DataFrame
scores = []
for i in range(len(models)):
    scores.extend([neutral_scores[i], positive_scores[i], negative_scores[i]])

data = pd.DataFrame({
    'Model': np.repeat(models, len(prompt_types)),
    'Prompt': prompt_types * len(models),
    'Skóre': scores
})

# Převedení sloupce 'Prompt' na kategorický typ s definovaným pořadím
data['Prompt'] = pd.Categorical(data['Prompt'], categories=prompt_types, ordered=True)

# 1. Graf - sloupcový pro srovnání skóre podle různých promptů (opravený)
fig1, ax1 = plt.subplots(figsize=(10, 6))
df_pivot = data.pivot(index='Model', columns='Prompt', values='Skóre')
df_pivot.plot(kind='bar', ax=ax1, width=0.8) # Zvětšení šířky sloupců
ax1.set_title('Celkové skóre LLM modelů podle typu promptu', fontsize=14, fontweight='bold')
ax1.set_xlabel('Model', fontsize=12)
ax1.set_ylabel('Celkové skóre (0-100)', fontsize=12)
ax1.set_ylim(0, 105) # Mírné navýšení limitu pro lepší vizualizaci
ax1.grid(axis='y', linestyle='--', alpha=0.7)
ax1.legend(title='Typ promptu', title_fontsize='10', fontsize='9')
ax1.tick_params(axis='x', rotation=45) # Otočení popisků modelů pro lepší čitelnost
plt.tight_layout()
plt.savefig('llm_code_review_comparison_bar.png', dpi=300, bbox_inches='tight')
plt.close(fig1)
print("Sloupcový graf byl úspěšně vytvořen a uložen jako 'llm_code_review_comparison_bar.png'")

# Data pro druhý graf - procentuální pokles
prompt_differences_values = np.array(neutral_scores) - np.array(positive_scores)
percentage_decrease = (prompt_differences_values / np.array(neutral_scores)) * 100

# 2. Graf - procentuální pokles výkonu při pozitivním promptu
fig2, ax2 = plt.subplots(figsize=(8, 6))
x_pos = np.arange(len(models))
bar_width = 0.5

bars = ax2.bar(x_pos, percentage_decrease, bar_width, color='firebrick', alpha=0.85)
ax2.set_title('Pokles výkonu při pozitivním promptu\n(oproti neutrálnímu)', fontsize=14, fontweight='bold')
ax2.set_xlabel('Model', fontsize=12)
ax2.set_ylabel('Pokles skóre (%)', fontsize=12)
ax2.set_xticks(x_pos)
ax2.set_xticklabels(models)
ax2.grid(axis='y', linestyle='--', alpha=0.7)
ax2.set_ylim(0, max(percentage_decrease) * 1.15 if max(percentage_decrease) > 0 else 10) # Dynamický horní limit

# Přidání hodnot na vrchol sloupců
for i, v in enumerate(percentage_decrease):
    ax2.text(i, v + 0.5, f'{v:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig('llm_positive_prompt_decrease.png', dpi=300, bbox_inches='tight')
plt.close(fig2)
print("Graf poklesu výkonu byl úspěšně vytvořen a uložen jako 'llm_positive_prompt_decrease.png'")


# 3. Graf - čárový graf pro trendy skóre
fig3, ax3 = plt.subplots(figsize=(10, 6))
for model_name in models:
    model_data = data[data['Model'] == model_name]
    ax3.plot(model_data['Prompt'], model_data['Skóre'], marker='o', linestyle='-', linewidth=2, label=model_name)

ax3.set_title('Trendy skóre LLM modelů napříč typy promptů', fontsize=14, fontweight='bold')
ax3.set_xlabel('Typ promptu', fontsize=12)
ax3.set_ylabel('Celkové skóre (0-100)', fontsize=12)
ax3.set_ylim(0, 105)
ax3.grid(axis='y', linestyle='--', alpha=0.7)
ax3.legend(title='Model', title_fontsize='10', fontsize='9', loc='best') # 'best' umístění legendy
plt.tight_layout()
plt.savefig('llm_code_review_trends_line.png', dpi=300, bbox_inches='tight')
plt.close(fig3)
print("Čárový graf byl úspěšně vytvořen a uložen jako 'llm_code_review_trends_line.png'")
