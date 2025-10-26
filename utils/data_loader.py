import pandas as pd

def load_nfhs_data(csv_path="data/nfhs_data.csv"):
    """
    Load and clean NFHS dataset
    """
    df = pd.read_csv(csv_path)

    # Normalize column names
    df.columns = [
        col.lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("-", "_")
        .replace("(", "")
        .replace(")", "")
        for col in df.columns
    ]

    # Convert numeric columns
    numeric_cols = df.columns[2:]  # first 2 cols: states_uts, area
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

def get_column_info():
    """
    Return mapping of column names to descriptions
    """
    info = {
        "number_of_households_surveyed": "Number of Households surveyed",
        "number_of_women_age_15_49_years_interviewed": "Number of Women age 15-49 years interviewed",
        "number_of_men_age_15_54_years_interviewed": "Number of Men age 15-54 years interviewed",
        "female_population_age_6_years_who_ever_attended_school_%": "Female population age 6+ who ever attended school (%)",
        "population_below_age_15_years_%": "Population below age 15 (%)",
        "sex_ratio_of_the_total_population": "Sex ratio of the total population (females per 1,000 males)",
        "sex_ratio_at_birth_for_children_born_in_the_last_five_years": "Sex ratio at birth for children born in the last five years",
        "children_under_age_5_years_whose_birth_was_registered_with_the_civil_authority_%": "Children under age 5 years whose birth was registered (%)",
        "deaths_in_the_last_3_years_registered_with_the_civil_authority_%": "Deaths in last 3 years registered (%)",
        "population_living_in_households_with_electricity_%": "Population living in households with electricity (%)",
        "population_living_in_households_with_an_improved_drinking_water_source1_%": "Population living in households with improved drinking-water source (%)",
        "population_living_in_households_that_use_an_improved_sanitation_facility2_%": "Population living in households that use improved sanitation facility (%)",
        "households_using_clean_fuel_for_cooking3_%": "Households using clean fuel for cooking (%)",
        "households_using_iodized_salt_%": "Households using iodized salt (%)",
        "households_with_any_usual_member_covered_under_a_health_insurance_financing_scheme_%": "Households with any member covered under health insurance (%)",
        "children_age_5_years_who_attended_pre_primary_school_during_the_school_year_2019_20_%": "Children age 5 who attended pre-primary school (%)",
        "women_age_15_49_who_are_literate4_%": "Women (15-49) who are literate (%)",
        "men_age_15_49_who_are_literate4_%": "Men (15-49) who are literate (%)",
        # Continue adding all remaining columns similarly...
        "women_age_15_years_and_above_with_high_141_160_mg_dl_blood_sugar_level": "Women age 15+ with high (141-160 mg/dl) blood sugar",
        "men_age_15_years_and_above_wih_high_141_160_mg_dl_blood_sugar_level": "Men age 15+ with high (141-160 mg/dl) blood sugar",
        # Add all remaining indicators from your list in same format
    }
    return info
