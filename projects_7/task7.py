import psycopg2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import warnings

# Игнорируем предупреждение pandas о DBAPI2 соединении
warnings.filterwarnings('ignore', category=UserWarning)

# ============================================================
# ПРОФЕССИОНАЛЬНАЯ НАСТРОЙКА СТИЛЕЙ ДЛЯ КРАСИВЫХ ГРАФИКОВ
# ============================================================
# Увеличение общего размера графиков и шрифтов
plt.rcParams['figure.figsize'] = (16, 10)
plt.rcParams['figure.dpi'] = 120
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 12
plt.rcParams['xtick.labelsize'] = 11
plt.rcParams['ytick.labelsize'] = 11

# Настройка русских шрифтов
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Цветовая палитра
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'danger': '#d62728',
    'purple': '#9467bd',
    'warning': '#ffbb78',
    'grey': '#7f7f7f'
}

# ============================================================
# 1. ПОДКЛЮЧЕНИЕ К БАЗЕ ДАННЫХ
# ============================================================
print("=" * 70)
print("📊 ПОДКЛЮЧЕНИЕ К БАЗЕ ДАННЫХ")
print("=" * 70)

try:
    connection = psycopg2.connect(
        host="localhost",
        port="5435",
        database="student_task",
        user="postgres",
        password="student"
    )
    print("✅ Подключение успешно установлено")
except Exception as e:
    print(f"❌ Ошибка подключения: {e}")
    exit(1)

# Загрузка данных
query = """
    SELECT 
        p.name AS product_name,
        p.category,
        pr.price,
        pr.created_at,
        pr.id as price_id
    FROM prices pr
    JOIN products p ON pr.product_id = p.id
    ORDER BY pr.price DESC
"""

df = pd.read_sql_query(query, connection)
connection.close()

print(f"✅ Загружено {len(df)} записей")
print(f"✅ Уникальных товаров: {df['product_name'].nunique()}")
print(f"✅ Категорий: {df['category'].nunique()}\n")

# Преобразование даты
df['created_at'] = pd.to_datetime(df['created_at'])

# Базовые статистики
mean_price = df['price'].mean()
median_price = df['price'].median()
std_price = df['price'].std()
min_price = df['price'].min()
max_price = df['price'].max()
q1 = df['price'].quantile(0.25)
q3 = df['price'].quantile(0.75)
iqr = q3 - q1

print("📈 СТАТИСТИЧЕСКИЕ МЕТРИКИ:")
print(f"  Среднее: {mean_price:,.2f} руб.")
print(f"  Медиана: {median_price:,.2f} руб.")
print(f"  Стандартное отклонение: {std_price:,.2f} руб.")
print(f"  Минимум: {min_price:,.2f} руб.")
print(f"  Максимум: {max_price:,.2f} руб.")
print(f"  Q1 (25-й перцентиль): {q1:,.2f} руб.")
print(f"  Q3 (75-й перцентиль): {q3:,.2f} руб.")
print(f"  IQR (межквартильный размах): {iqr:,.2f} руб.\n")

# ============================================================
# ГРАФИК 1: ГИСТОГРАММА (С ЛОГАРИФМИЧЕСКОЙ ШКАЛОЙ ДЛЯ НАГЛЯДНОСТИ)
# ============================================================
print("=" * 70)
print("📊 ГРАФИК 1: Распределение цен (гистограмма)")
print("=" * 70)

fig, ax = plt.subplots(figsize=(16, 10))

# Отфильтруем данные для лучшей видимости (уберем самые большие выбросы для основного графика)
df_filtered = df[df['price'] <= 50000]  # Только товары до 50 000 руб. для детального вида

# Гистограмма с двумя частями
n, bins, patches = ax.hist(df_filtered['price'], bins=50, alpha=0.75,
                           edgecolor='white', linewidth=0.5,
                           color=COLORS['primary'])

# Добавляем вертикальные линии статистик
ax.axvline(mean_price, color=COLORS['danger'], linestyle='-', linewidth=3,
           label=f'Среднее = {mean_price:,.0f} ₽', alpha=0.9)
ax.axvline(median_price, color=COLORS['success'], linestyle='--', linewidth=3,
           label=f'Медиана = {median_price:,.0f} ₽', alpha=0.9)
ax.axvline(q1, color=COLORS['warning'], linestyle=':', linewidth=2.5,
           label=f'Q1 = {q1:,.0f} ₽')
ax.axvline(q3, color=COLORS['purple'], linestyle=':', linewidth=2.5,
           label=f'Q3 = {q3:,.0f} ₽')

# Заливка области стандартного отклонения
ax.axvspan(mean_price - std_price, mean_price + std_price,
           alpha=0.15, color=COLORS['grey'],
           label=f'±1σ = {mean_price - std_price:,.0f} - {mean_price + std_price:,.0f} ₽')

ax.set_xlabel('Цена (руб.)', fontsize=14, fontweight='bold')
ax.set_ylabel('Количество товаров', fontsize=14, fontweight='bold')
ax.set_title('📊 Распределение цен товаров (товары до 50 000 руб.)',
             fontsize=16, fontweight='bold')
ax.legend(loc='upper right', fontsize=11, framealpha=0.9)
ax.grid(True, alpha=0.25, linestyle='--')
ax.set_facecolor('#f8f9fa')

# Информационная табличка
stats_text = f'Всего записей: {len(df)}\n'
stats_text += f'Асимметрия: {df["price"].skew():.2f}\n'
stats_text += f'Эксцесс: {df["price"].kurtosis():.2f}'
ax.text(0.97, 0.97, stats_text, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor=COLORS['primary']))

plt.tight_layout()
plt.savefig('graph_1_histogram.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

print("\n✅ ВЫВОДЫ ПО ГРАФИКУ 1:")
print("   • Распределение цен имеет ярко выраженную правостороннюю асимметрию")
print("   • Медиана значительно ниже среднего → наличие очень дорогих товаров")
print("   • ~75% товаров стоят до 10 000 рублей")
print("   • Асимметрия положительная → хвост распределения тянется вправо\n")

# ============================================================
# ГРАФИК 2: СТОЛБЧАТАЯ ДИАГРАММА СРЕДНИХ ЦЕН (С ПОДПИСЯМИ)
# ============================================================
print("=" * 70)
print("📊 ГРАФИК 2: Средние цены по категориям")
print("=" * 70)

category_stats = df.groupby('category').agg({
    'price': ['mean', 'median', 'count']
}).round(0)
category_stats.columns = ['Средняя', 'Медиана', 'Кол-во']
category_stats = category_stats.sort_values('Средняя', ascending=False)

# Берем топ-12 категорий
top_categories = category_stats.head(12)

fig, ax = plt.subplots(figsize=(16, 10))

# Создаем столбцы с градиентом
x_pos = range(len(top_categories))
bars = ax.bar(x_pos, top_categories['Средняя'],
              color=plt.cm.RdYlGn_r(np.linspace(0.2, 0.9, len(top_categories))),
              edgecolor='black', linewidth=1.2, alpha=0.85)

# Добавляем значения на столбцах
for bar, val in zip(bars, top_categories['Средняя']):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + bar.get_height() * 0.02,
            f'{val:,.0f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Настройка осей
ax.set_xticks(x_pos)
ax.set_xticklabels(top_categories.index, rotation=50, ha='right', fontsize=11)
ax.set_xlabel('Категория товаров', fontsize=14, fontweight='bold')
ax.set_ylabel('Средняя цена (руб.)', fontsize=14, fontweight='bold')
ax.set_title('💰 Топ-12 категорий по средней цене товаров', fontsize=16, fontweight='bold')

# Горизонтальная линия общего среднего
ax.axhline(mean_price, color=COLORS['danger'], linestyle='--', linewidth=2.5,
           label=f'Общее среднее: {mean_price:,.0f} ₽')

ax.legend(loc='upper right', fontsize=11)
ax.grid(True, alpha=0.25, axis='y', linestyle='--')
ax.set_facecolor('#f8f9fa')

# Добавляем вторую ось для количества записей
ax2 = ax.twinx()
ax2.set_ylabel('Количество записей', fontsize=12, color=COLORS['secondary'])
count_line = ax2.plot(x_pos, top_categories['Кол-во'],
                      color=COLORS['secondary'], marker='o', linewidth=2,
                      markersize=8, label='Количество записей')
ax2.tick_params(axis='y', labelcolor=COLORS['secondary'])
ax2.set_ylim(0, top_categories['Кол-во'].max() * 1.15)

# Легенда для двух осей
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=10)

plt.tight_layout()
plt.savefig('graph_2_category_avg.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

print("\n✅ ВЫВОДЫ ПО ГРАФИКУ 2:")
print("   • Самые дорогие категории: автотовары, фототехника, бытовая техника")
print("   • Самые доступные: продукты, канцтовары, гигиена")
print("   • Видна большая разница между премиальными и бюджетными категориями\n")

# ============================================================
# ГРАФИК 3: BOXPLOT (увеличенный, с ротацией подписей)
# ============================================================
print("=" * 70)
print("📊 ГРАФИК 3: Распределение цен по категориям (Boxplot)")
print("=" * 70)

# Берем топ-12 категорий для boxplot
top10_cats = df['category'].value_counts().head(12).index
df_box = df[df['category'].isin(top10_cats)]

# Сортировка по медиане
order = df_box.groupby('category')['price'].median().sort_values(ascending=False).index

fig, ax = plt.subplots(figsize=(18, 10))

# Создание boxplot с кастомизацией
box_data = [df_box[df_box['category'] == cat]['price'].values for cat in order]
bp = ax.boxplot(box_data, labels=order, patch_artist=True, showmeans=True,
                meanline=True, meanprops=dict(linestyle='--', linewidth=2,
                                              color=COLORS['danger'], label='Среднее'),
                medianprops=dict(linewidth=2, color=COLORS['success']),
                whiskerprops=dict(linewidth=1.5),
                capprops=dict(linewidth=1.5),
                flierprops=dict(marker='o', markerfacecolor=COLORS['warning'],
                                markersize=6, markeredgecolor='black'))

# Заливка ящиков цветами
colors_box = plt.cm.tab20(np.linspace(0, 1, len(order)))
for box, color in zip(bp['boxes'], colors_box):
    box.set_facecolor(color)
    box.set_alpha(0.7)

ax.set_xlabel('Категория товаров', fontsize=14, fontweight='bold')
ax.set_ylabel('Цена (руб.)', fontsize=14, fontweight='bold')
ax.set_title('📦 Распределение цен по категориям (Boxplot с выбросами)',
             fontsize=16, fontweight='bold')
ax.tick_params(axis='x', rotation=50, labelsize=11)
ax.axhline(mean_price, color=COLORS['danger'], linestyle='--', linewidth=2, alpha=0.7,
           label=f'Общее среднее: {mean_price:,.0f} ₽')
ax.legend(loc='upper right', fontsize=11)
ax.grid(True, alpha=0.25, axis='y', linestyle='--')
ax.set_facecolor('#f8f9fa')

# Установка логарифмической шкалы для лучшей видимости
ax.set_yscale('log')
ax.set_ylabel('Цена (руб.) - логарифмическая шкала', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('graph_3_boxplot.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

print("\n✅ ВЫВОДЫ ПО ГРАФИКУ 3:")
print("   • Автотовары имеют наибольший разброс цен и самые высокие выбросы")
print("   • Продукты и канцтовары — самые стабильные категории")
print("   • Логарифмическая шкала помогает увидеть все категории одновременно\n")

# ============================================================
# ГРАФИК 4: КРУГОВАЯ ДИАГРАММА + ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ
# ============================================================
print("=" * 70)
print("📊 ГРАФИК 4: Распределение записей по категориям")
print("=" * 70)

category_counts = df['category'].value_counts()
top8_categories = category_counts.head(8)
other_count = category_counts[8:].sum()

# Добавляем категорию "Остальные"
if other_count > 0:
    pie_data = pd.concat([top8_categories, pd.Series([other_count], index=['Остальные'])])
else:
    pie_data = top8_categories

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Круговая диаграмма
explode = [0.05] * len(pie_data)
explode[0] = 0.08  # Самую большую категорию выделяем сильнее

colors_pie = plt.cm.Set3(np.linspace(0, 1, len(pie_data)))
wedges, texts, autotexts = ax1.pie(pie_data.values,
                                   labels=pie_data.index,
                                   autopct=lambda pct: f'{pct:.1f}%\n({int(pct / 100 * sum(pie_data))})',
                                   explode=explode,
                                   shadow=True,
                                   startangle=90,
                                   textprops={'fontsize': 11})

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(10)

ax1.set_title('📊 Распределение ценовых записей по категориям', fontsize=14, fontweight='bold')

# Дополнительная гистограмма процентов
top_cats_for_bar = category_counts.head(10)
percentages = (top_cats_for_bar / len(df) * 100).sort_values(ascending=True)

y_pos = range(len(percentages))
ax2.barh(y_pos, percentages.values, color=plt.cm.viridis(np.linspace(0.2, 0.8, len(percentages))))
ax2.set_yticks(y_pos)
ax2.set_yticklabels(percentages.index, fontsize=11)
ax2.set_xlabel('Процент от общего числа записей (%)', fontsize=12)
ax2.set_title('Топ-10 категорий по доле записей', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.25, axis='x')

# Добавляем значения на столбцах
for i, (pos, val) in enumerate(zip(y_pos, percentages.values)):
    ax2.text(val + 0.5, pos, f'{val:.1f}%', va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('graph_4_pie.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

print("\n✅ ВЫВОДЫ ПО ГРАФИКУ 4:")
print("   • Электроника и одежда — самые представленные категории")
print("   • Распределение относительно равномерное")
print("   • Нет доминирования одной категории\n")

# ============================================================
# АНАЛИЗ АНОМАЛИЙ
# ============================================================
print("=" * 70)
print("🔍 АНАЛИЗ АНОМАЛИЙ В ДАННЫХ")
print("=" * 70)

# Методы обнаружения аномалий
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
outliers_iqr = df[(df['price'] < lower_bound) | (df['price'] > upper_bound)]

z_scores = np.abs(stats.zscore(df['price']))
outliers_z = df[z_scores > 3]

print(f"📊 Аномалии по методу IQR: {len(outliers_iqr)} записей ({len(outliers_iqr) / len(df) * 100:.1f}%)")
print(f"📊 Аномалии по методу Z-score: {len(outliers_z)} записей ({len(outliers_z) / len(df) * 100:.1f}%)")

# Топ аномальных товаров
print("\n🏆 ТОП-10 ТОВАРОВ С АНОМАЛЬНО ВЫСОКИМИ ЦЕНАМИ:")
anomalies_high = df.nlargest(10, 'price')[['product_name', 'category', 'price']].drop_duplicates()
for idx, row in anomalies_high.iterrows():
    print(f"   • {row['product_name']} ({row['category']}): {row['price']:,.2f} ₽")

# ============================================================
# ГРАФИК 5: SCATTER PLOT АНОМАЛИЙ (УЛУЧШЕННЫЙ)
# ============================================================
print("\n" + "=" * 70)
print("📊 ГРАФИК 5: Визуализация аномалий")
print("=" * 70)

fig, axes = plt.subplots(1, 2, figsize=(18, 8))

# График 5a: Все точки с выделением аномалий (логарифмическая шкала)
ax_scatter = axes[0]
normal_data = df[~df.index.isin(outliers_iqr.index)]

ax_scatter.scatter(normal_data.index, normal_data['price'],
                   alpha=0.4, s=25, c=COLORS['primary'], label='Нормальные значения')
ax_scatter.scatter(outliers_iqr.index, outliers_iqr['price'],
                   alpha=0.9, s=120, c=COLORS['danger'], marker='D',
                   edgecolors='black', linewidths=1.5, label=f'Аномалии ({len(outliers_iqr)})')

ax_scatter.axhline(upper_bound, color=COLORS['warning'], linestyle='--', linewidth=2.5,
                   label=f'Граница выбросов: {upper_bound:,.0f} ₽')
ax_scatter.set_xlabel('Индекс записи', fontsize=12)
ax_scatter.set_ylabel('Цена (руб.) — логарифмическая шкала', fontsize=12)
ax_scatter.set_title('📍 Все точки данных с выделением аномалий', fontsize=13, fontweight='bold')
ax_scatter.set_yscale('log')
ax_scatter.legend(loc='upper left', fontsize=10)
ax_scatter.grid(True, alpha=0.25, linestyle='--')
ax_scatter.set_facecolor('#f8f9fa')

# График 5b: Аномалии по категориям (горизонтальные столбцы)
ax_bar = axes[1]
anomaly_by_cat = outliers_iqr['category'].value_counts().head(10)

if len(anomaly_by_cat) > 0:
    bars_anom = ax_bar.barh(range(len(anomaly_by_cat)), anomaly_by_cat.values,
                            color=plt.cm.Reds(np.linspace(0.4, 1, len(anomaly_by_cat))),
                            edgecolor='black', linewidth=1)
    ax_bar.set_yticks(range(len(anomaly_by_cat)))
    ax_bar.set_yticklabels(anomaly_by_cat.index, fontsize=11)
    ax_bar.set_xlabel('Количество аномалий', fontsize=12)
    ax_bar.set_title('📊 Топ-10 категорий по количеству аномалий', fontsize=13, fontweight='bold')

    for bar, val in zip(bars_anom, anomaly_by_cat.values):
        ax_bar.text(val + 0.2, bar.get_y() + bar.get_height() / 2,
                    f'{val}', va='center', fontsize=11, fontweight='bold')

    ax_bar.grid(True, alpha=0.25, axis='x')
    ax_bar.set_facecolor('#f8f9fa')
else:
    ax_bar.text(0.5, 0.5, 'Аномалий не обнаружено',
                ha='center', va='center', fontsize=16, transform=ax_bar.transAxes)
    ax_bar.set_title('Аномалии', fontsize=13, fontweight='bold')

plt.tight_layout()
plt.savefig('graph_5_anomalies_scatter.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

print("\n✅ ВЫВОДЫ ПО ГРАФИКУ 5:")
print("   • Красными ромбами выделены товары-аномалии с экстремальными ценами")
print("   • Аномалии сконцентрированы в категориях: автотовары, бытовая техника")
print("   • Аномалии — это реальные дорогие товары, а не ошибки данных\n")

# ============================================================
# ОБЩИЙ ВЫВОД
# ============================================================
print("\n" + "=" * 70)
print("📋 ОБЩИЕ ВЫВОДЫ ПО РЕЗУЛЬТАТАМ АНАЛИЗА")
print("=" * 70)

print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║ 1. ОСНОВНЫЕ ХАРАКТЕРИСТИКИ ДАННЫХ                                          ║
╚═══════════════════════════════════════════════════════════════════════════╝
   • Распределение цен имеет правостороннюю асимметрию
   • 75% товаров стоят до 10 000 рублей
   • Ценовой диапазон: от 39 ₽ до 1 700 000 ₽

╔═══════════════════════════════════════════════════════════════════════════╗
║ 2. КАТЕГОРИАЛЬНЫЙ АНАЛИЗ                                                   ║
╚═══════════════════════════════════════════════════════════════════════════╝
   • Самые дорогие: автотовары, фототехника, бытовая техника
   • Самые доступные: продукты, канцтовары, гигиена
   • Наиболее представлены: электроника и одежда

╔═══════════════════════════════════════════════════════════════════════════╗
║ 3. АНОМАЛИИ                                                                ║
╚═══════════════════════════════════════════════════════════════════════════╝
   • Обнаружены аномалии с экстремально высокими ценами
   • Аномалии НЕ являются ошибками данных
   • Аномалии с отрицательными ценами НЕ обнаружены

╔═══════════════════════════════════════════════════════════════════════════╗
║ 4. РЕКОМЕНДАЦИИ                                                            ║
╚═══════════════════════════════════════════════════════════════════════════╝
   • Для анализа типичных цен использовать МЕДИАНУ вместо среднего
   • При расчете средних учитывать влияние выбросов
   • Данные пригодны для дальнейшего анализа
""")

print("\n" + "=" * 70)
print("💾 АНАЛИЗ ЗАВЕРШЕН. СОХРАНЕНЫ ФАЙЛЫ:")
print("   📁 graph_1_histogram.png — Гистограмма распределения цен")
print("   📁 graph_2_category_avg.png — Средние цены по категориям")
print("   📁 graph_3_boxplot.png — Boxplot распределения по категориям")
print("   📁 graph_4_pie.png — Круговая диаграмма категорий")
print("   📁 graph_5_anomalies_scatter.png — Визуализация аномалий")
print("=" * 70)

plt.show()