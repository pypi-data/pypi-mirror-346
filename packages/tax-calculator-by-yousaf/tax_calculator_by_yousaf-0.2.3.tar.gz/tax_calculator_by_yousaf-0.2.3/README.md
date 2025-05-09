# Indian Tax Calculator FY 2025-26

![Version](https://img.shields.io/badge/version-0.2.3-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A comprehensive calculator to compute income tax for India based on both old and new tax regimes for Financial Year 2025-26, reflecting the latest changes from Budget 2025.

## Features

- Calculate tax based on either monthly or yearly salary inputs
- Support for both old and new tax regimes with accurate 2025-26 tax slabs
- Detailed breakdown of tax calculation
- Monthly mode includes options for:
  - Consolidated additional incentives/allowances (performance pay, special allowance, etc.)
  - One-time bonus/variable pay (not multiplied by 12)
  - Consolidated additional deductions (Professional Tax, Labor Welfare Fund, etc.)
  - Detailed calculations for bonus month including in-hand amount
- Yearly mode provides annual salary calculation
- Considers standard deduction, PF, LTA, HRA, and other components
- Proper handling of EPF contributions in new tax regime
- Additional tax-saving deductions for old regime (80C, 80D, 80E)
- Computes in-hand salary after all deductions
- Easy-to-use command-line interface with helpful notes

## Installation

You can install the package directly from PyPI:

```bash
pip install tax_calculator_by_yousaf
```

Alternatively, you can install directly from GitHub:

```bash
pip install git+https://github.com/yousafkhamza/tax_calculator_by_yousaf.git
```

## Usage

After installation, you can run the calculator directly from the command line:

```bash
tax-calculator
```

Or import it in your Python code:

```python
from tax_calculator import calculate_tax_2025_26

calculate_tax_2025_26()
```

## Tax Calculation Details

### New Regime (Default for FY 2025-26)

- Standard Deduction: ₹75,000
- Tax Slabs:
  - Up to ₹4,00,000: No tax
  - ₹4,00,001 to ₹8,00,000: 5%
  - ₹8,00,001 to ₹12,00,000: 10%
  - ₹12,00,001 to ₹16,00,000: 15%
  - ₹16,00,001 to ₹20,00,000: 20%
  - ₹20,00,001 to ₹24,00,000: 25%
  - Above ₹24,00,000: 30%
- Section 87A rebate up to ₹60,000 for income up to ₹12,00,000
  - Effective zero tax for income up to ₹12,00,000
  - For salaried individuals, effective zero tax for income up to ₹12,75,000 (due to standard deduction)
- Important: EPF contributions are NOT tax-exempt under the new regime

### Old Regime

- Standard Deduction: ₹50,000
- Tax Slabs:
  - Up to ₹2,50,000: No tax
  - ₹2,50,001 to ₹5,00,000: 5%
  - ₹5,00,001 to ₹10,00,000: 20%
  - Above ₹10,00,000: 30%
- Section 87A rebate applicable for income up to ₹5,00,000 (₹12,500 rebate)
- Additional deductions available (80C, 80D, 80E, etc.)
- EPF contributions are tax-exempt

### Surcharge Details

- 10% for income between ₹50 lakhs and ₹1 crore
- 15% for income between ₹1 crore and ₹2 crore
- 25% for income between ₹2 crore and ₹5 crore
- 37% for income above ₹5 crore (25% under new regime)
- Health and Education Cess of 4% applicable on all tax amounts

## EPF Treatment in New Tax Regime

- Employer's EPF contribution (up to 12% of salary) remains tax-exempt
- Combined employer contributions to EPF, NPS, and superannuation funds are tax-exempt up to ₹7.5 lakh
- Employee's EPF contribution is NOT eligible for tax deduction under the new regime
- Interest earned on EPF up to ₹2.5 lakh contribution remains tax-exempt

## When to Choose Which Regime?

- **New Regime**: Beneficial for individuals with fewer tax-saving investments or deductions, especially those with income above ₹15 lakhs
- **Old Regime**: May be more beneficial for individuals with significant tax-saving investments and deductions

## Command-Line Interface

The calculator guides you through a simple interactive process:

### Monthly Input Mode

1. Choose monthly input mode
2. Enter monthly salary components:
   - Basic Salary
   - HRA
   - Special Allowance
   - LTA
   - PF Contribution
   - Additional Incentives/Allowances
   - Additional Deductions (PT, LWF, etc.)
   - One-time Bonus/Variable Pay (not multiplied by 12)
3. Select tax regime
4. For old regime, enter additional deductions
5. View calculated monthly tax and in-hand salary
6. If bonus was entered, see detailed bonus month calculation including:
   - Gross salary for bonus month
   - Additional tax due to bonus
   - Total tax for bonus month
   - In-hand salary for bonus month
   - Updated annual total with bonus

### Yearly Input Mode

1. Choose yearly input mode
2. Enter yearly salary components:
   - Basic Salary
   - HRA
   - Special Allowance
   - LTA
   - PF Contribution
3. Select tax regime
4. For old regime, enter additional deductions
5. View calculated annual tax and in-hand salary
6. See note about calculating bonus in monthly mode

## Requirements

- Python 3.6 or higher

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Yousaf Khamza
