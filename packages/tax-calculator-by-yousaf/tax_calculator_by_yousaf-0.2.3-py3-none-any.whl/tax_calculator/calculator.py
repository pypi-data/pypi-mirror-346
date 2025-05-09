"""
Tax Calculator for FY 2025-26
A simple calculator to compute income tax for India based on old and new regimes.
"""

def calculate_tax_2025_26():
    """
    Main function to run the tax calculator interactively.
    Provides detailed breakdown of tax calculation for FY 2025-26.
    """
    print("\n===== Salary & Tax Calculator for FY 2025-26 =====\n")
    print("📝 NOTE: If any field is not applicable, you can leave it blank or enter 0")
    print("         All amounts should be entered as numbers only (with or without commas)")
    print("-" * 82)

    # Input Mode
    mode_choice = input("1 - Monthly\n2 - Yearly\nEnter your choice: ").strip()

    if mode_choice == "1":
        # Monthly inputs
        basic = get_float_input("\nEnter monthly Basic salary: ")
        hra = get_float_input("Enter monthly HRA: ")
        special_allowance = get_float_input("Enter monthly Special Allowance: ")
        lta = get_float_input("Enter monthly LTA: ")
        pf = get_float_input("Enter monthly PF Contribution: ")
        additional_incentives = get_float_input("Enter monthly Additional Incentives/Allowance (Internet, Driver, etc. total): ")
        additional_deductions = get_float_input("Enter monthly Additional Deductions (PT, LWF, etc. total): ")
        
        # One-time bonus/variable pay (not multiplied by 12)
        one_time_bonus = get_float_input("Enter One-time Bonus/Variable Pay (will not be multiplied by 12): ")

        monthly_gross = basic + hra + special_allowance + lta + additional_incentives
        monthly_deductions = pf + additional_deductions

        # Annual calculations without bonus
        gross_annual = (12 * monthly_gross)
        deductions_annual = 12 * monthly_deductions
        annual_lta = 12 * lta
        
        # Annual with one-time bonus
        gross_annual_with_bonus = gross_annual + one_time_bonus
        
    elif mode_choice == "2":
        # Annual inputs
        basic = get_float_input("\nEnter annual Basic salary: ")
        hra = get_float_input("Enter annual HRA: ")
        special_allowance = get_float_input("Enter annual Special Allowance: ")
        lta = get_float_input("Enter annual LTA: ")
        pf = get_float_input("Enter annual PF Contribution: ")
        
        # Regular annual income
        gross_annual = basic + hra + special_allowance + lta
        deductions_annual = pf
        annual_lta = lta
        
        # Monthly values (for consistent calculations)
        monthly_gross = gross_annual / 12
        monthly_deductions = deductions_annual / 12
        one_time_bonus = 0  # No one-time bonus in yearly mode
        gross_annual_with_bonus = gross_annual
    else:
        print("Invalid input. Please enter 1 or 2.")
        return

    # Additional tax-saving deductions for old regime
    if regime := input("\nChoose tax regime (old/new): ").strip().lower() or "new":
        if regime == "old":
            print("\n--- Additional deductions (applicable only for old regime) ---")
            medical_insurance = get_float_input("Enter Medical Insurance Premium (80D): ")
            education_loan = get_float_input("Enter Education Loan Interest (80E): ")
            investment_80c = get_float_input("Enter Investment Deductions (80C): ")
            
            additional_deductions = medical_insurance + education_loan + investment_80c
        else:
            additional_deductions = 0
    else:
        regime = "new"
        additional_deductions = 0

    # Standard deduction amount depends on regime
    standard_deduction = 50000 if regime == "old" else 75000

    # Calculate tax without bonus
    print(f"\n--- Regular Salary Calculation (without Bonus) ---")
    print(f"Annual Gross (without Bonus): ₹{gross_annual:,.2f}")
    
    if regime == "old":
        print(f"Annual Deductions (excl. Tax): ₹{deductions_annual:,.2f}")
        if additional_deductions > 0:
            print(f"Additional Tax Saving Deductions: ₹{additional_deductions:,.2f}")
        
        # Taxable income calculation for OLD regime - all deductions apply
        taxable_income = gross_annual - standard_deduction - deductions_annual - annual_lta - additional_deductions
        taxable_income = max(0, taxable_income)
        print(f"Taxable Income (Old Regime) without Bonus: ₹{taxable_income:,.2f}")
        tax = calculate_old_regime_tax(taxable_income)
    else:
        # In new regime, ONLY standard deduction is allowed
        # PF contributions are NOT tax-exempt under new regime
        print(f"Standard Deduction: ₹{standard_deduction:,.2f}")
        print(f"Note: Under new regime, EPF contributions are not eligible for tax deduction")
        
        # Taxable income calculation for NEW regime - only standard deduction
        taxable_income = gross_annual - standard_deduction
        taxable_income = max(0, taxable_income)
        print(f"Taxable Income (New Regime) without Bonus: ₹{taxable_income:,.2f}")
        tax = calculate_new_regime_tax(taxable_income)
    
    print(f"Annual Tax (without Bonus): ₹{tax:,.2f}")
    monthly_tax = round(tax / 12, 2)
    
    # Calculate regular in-hand amounts
    in_hand_monthly = round(monthly_gross - monthly_deductions - monthly_tax, 2)
    in_hand_annual = round(gross_annual - deductions_annual - tax, 2)

    # Regular summary section
    print("\n--- Regular Salary Summary ---")
    print(f"👉 Monthly Gross Salary: ₹{monthly_gross:,.2f}")
    print(f"👉 Monthly Tax Deduction (TDS): ₹{monthly_tax:,.2f}")
    print(f"💸 In-hand Monthly Salary: ₹{in_hand_monthly:,.2f}")
    print(f"💸 In-hand Annual Salary (12 months): ₹{in_hand_annual:,.2f}")
    
    # Add note for yearly mode about calculating bonus in monthly mode
    if mode_choice == "2":
        print("\n📝 NOTE: To calculate salary with bonus or variable pay, please use Monthly mode (Option 1)")
        print("         and enter your bonus amount in the 'One-time Bonus/Variable Pay' field.")
        print("         This will provide you with detailed tax calculations for your bonus month.")
    
    # If one-time bonus is provided, calculate its impact
    if one_time_bonus > 0 and mode_choice == "1":
        print(f"\n--- Bonus Month Calculation ---")
        print(f"One-time Bonus Amount: ₹{one_time_bonus:,.2f}")
        
        # Calculate the gross for bonus month
        gross_bonus_month = monthly_gross + one_time_bonus
        print(f"Gross Salary for Bonus Month: ₹{gross_bonus_month:,.2f}")
        
        # Calculate tax with bonus included
        if regime == "old":
            taxable_income_with_bonus = gross_annual_with_bonus - standard_deduction - deductions_annual - annual_lta - additional_deductions
            taxable_income_with_bonus = max(0, taxable_income_with_bonus)
            tax_with_bonus = calculate_old_regime_tax(taxable_income_with_bonus)
        else:
            taxable_income_with_bonus = gross_annual_with_bonus - standard_deduction
            taxable_income_with_bonus = max(0, taxable_income_with_bonus)
            tax_with_bonus = calculate_new_regime_tax(taxable_income_with_bonus)
        
        # Calculate additional tax due to bonus
        additional_tax = tax_with_bonus - tax
        print(f"Additional Tax due to Bonus: ₹{additional_tax:,.2f}")
        
        # Calculate tax for bonus month
        bonus_month_tax = monthly_tax + additional_tax
        print(f"Total Tax for Bonus Month: ₹{bonus_month_tax:,.2f}")
        
        # Calculate in-hand for bonus month
        in_hand_bonus_month = gross_bonus_month - monthly_deductions - bonus_month_tax
        print(f"💰 In-hand Salary for Bonus Month: ₹{in_hand_bonus_month:,.2f}")
        
        # Total annual with bonus
        in_hand_annual_with_bonus = in_hand_annual + one_time_bonus - additional_tax
        print(f"\n--- Annual Total (with Bonus) ---")
        print(f"Total Annual In-hand Salary: ₹{in_hand_annual_with_bonus:,.2f}")

def get_float_input(prompt):
    """
    Helper function to get float input from user.
    """
    user_input = input(prompt).strip()
    if user_input == "" or user_input == "0":
        return 0.0
    return float(user_input.replace(",", ""))


def calculate_old_regime_tax(income):
    """
    Calculate tax under the old regime for FY 2025-26.
    """
    # Old regime tax slabs remain unchanged
    tax = 0
    if income <= 250000:
        tax = 0
    elif income <= 500000:
        tax = (income - 250000) * 0.05
    elif income <= 1000000:
        tax = 12500 + (income - 500000) * 0.2
    else:
        tax = 12500 + 100000 + (income - 1000000) * 0.3

    # Section 87A rebate (₹12,500) for income <= ₹5L
    if income <= 500000:
        tax = max(0, tax - 12500)

    return round(tax + tax * 0.04, 2)  # 4% cess


def calculate_new_regime_tax(income):
    """
    Calculate tax under the new regime for FY 2025-26.
    """
    # Updated new regime tax slabs for FY 2025-26
    tax = 0
    
    if income <= 400000:
        tax = 0
    elif income <= 800000:
        tax = (income - 400000) * 0.05
    elif income <= 1200000:
        tax = 20000 + (income - 800000) * 0.10
    elif income <= 1600000:
        tax = 20000 + 40000 + (income - 1200000) * 0.15
    elif income <= 2000000:
        tax = 20000 + 40000 + 60000 + (income - 1600000) * 0.20
    elif income <= 2400000:
        tax = 20000 + 40000 + 60000 + 80000 + (income - 2000000) * 0.25
    else:
        tax = 20000 + 40000 + 60000 + 80000 + 100000 + (income - 2400000) * 0.30

    # Section 87A rebate up to ₹60,000 for income <= ₹12L
    if income <= 1200000:
        tax = max(0, tax - 60000)

    return round(tax + tax * 0.04, 2)  # 4% cess


def calculate_surcharge(income, tax):
    """
    Calculate surcharge based on income level.
    """
    if income > 5000000:  # > 5 crore
        surcharge_rate = 0.25 if regime == "new" else 0.37
        return tax * surcharge_rate
    elif income > 2000000:  # > 2 crore
        return tax * 0.25
    elif income > 1000000:  # > 1 crore
        return tax * 0.15
    elif income > 500000:   # > 50 lakh
        return tax * 0.10
    else:
        return 0


def main():
    """
    Entry point for the command-line script.
    Handles exceptions gracefully and provides user-friendly error messages.
    """
    try:
        calculate_tax_2025_26()
    except KeyboardInterrupt:
        print("\nTax calculation canceled.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")


if __name__ == "__main__":
    main()