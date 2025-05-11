# SNU-DHC

## Description
`DemoTable` generates baseline characteristic tables for medical studies and exports them to Excel.
It supports continuous and categorical variables, grouping, and automatic p-value calculation.

### Parameters:

- `df`: Input pandas DataFrame.
- `table_name`: Title for the Excel sheet.
- `variables`: List of dictionaries defining the variables to display.
- `group_variable`: Optional column to group comparisons.
- `group_labels`: Display labels for group values.
- `show_total`: Whether to show the total column.
- `show_missing`: Whether to show missing counts for categorical variables.
- `percent_decimals`: Decimal places for percentages.
- `thousands_sep`: Use comma separator for each thousand numbers.
- `show_p_values`: Whether to include a p-value column.
- `p_value_decimals`: Fixed or automatic formatting for p-values.

### Test selection logic (for p-values):
- **Continuous (mean)**:
  - 2 groups: Welch's t-test (with checks and warnings for normality)
  - 3+ groups: ANOVA (with checks and warnings for normality and variance)
- **Continuous (median)**:
  - 2 groups: Mann-Whitney U test
  - 3+ groups: Kruskal-Wallis test
- **Categorical**:
  - Chi-square test by default
  - Fisher's exact test if 2x2 and <5 cell counts
## Usage Example
```python
from snu_dhc.tables import DemoTable
    
variables_config = [
    {"var": "age", "name": "Age", "type": "continuous", "stat": "median", "decimals": 0},
    {"var": "sex", "name": "Sex", "type": "categorical", "class_labels": {1: "Male", 0: "Female"}},
    {"var": "dm", "name": "Diabetes mellitus", "type": "categorical", "class_labels": {1: ""}},
    {"var": "init_rhythm", "name": "Initial rhythm", "type": "categorical", "class_labels": {1: "VF/VT", 2: "PEA", 3: "Asystole"}},
    {"var": "rti", "name": "RTI", "type": "continuous", "stat": "median", "decimals": 0},
]

table = DemoTable(
    df=ohca_group,
    table_name="Table 1. Baseline characteristics of study patients",
    variables=variables_config,
    group_variable="group",
    group_labels={"train": "Train", "val": "Validation", "test": "Test"}, 
    show_total=True,
    show_missing=True,
    percent_decimals=1,
    thousands_sep=True,
    show_p_values=True,
    p_value_decimals="auto"
)

table.save("table1.xlsx")
```
