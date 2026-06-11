import os
import dotenv
from supabase import create_client, Client
from data import global_path_reference
dotenv.load_dotenv(f"{global_path_reference}/Program/bsed.env", override=True)

SUPABASE_URL = os.getenv("URL")
SUPABASE_KEY = os.getenv("KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
def create_account(username: str, password_hash: str, save_blob: str):

    # check if exists
    res = supabase.table("accounts") \
        .select("*") \
        .eq("username", username) \
        .execute()

    if res.data:
        print("Username already exists.")
        return False

    supabase.table("accounts").insert({
        "username": username,
        "password_hash": password_hash,
        "save_blob": save_blob,
        "cash_mantissa": 0,
        "cash_exponent": 0,
        "capsuled_singularity_mantissa": 0,
        "capsuled_singularity_exponent": 0
    }).execute()

    print("Account created.")
    return True

def get_account(username: str):

    res = supabase.table("accounts") \
        .select("*") \
        .eq("username", username) \
        .execute()

    return res.data

def update_save(
    username: str,
    save_blob: str,
    cash_mantissa: float,
    cash_exponent: int,
    capsuled_singularity_mantissa: float,
    capsuled_singularity_exponent: int
):

    supabase.table("accounts") \
        .update({
            "save_blob": save_blob,
            "cash_mantissa": cash_mantissa,
            "cash_exponent": cash_exponent,
            "capsuled_singularity_mantissa": capsuled_singularity_mantissa,
            "capsuled_singularity_exponent": capsuled_singularity_exponent
        }) \
        .eq("username", username) \
        .execute()
        
def delete_account(username: str):

    supabase.table("accounts") \
        .delete() \
        .eq("username", username) \
        .execute()

def get_top_cash(limit=10):

    res = supabase.table("accounts") \
        .select("username,cash_mantissa,cash_exponent") \
        .order("cash_exponent", desc=True) \
        .order("cash_mantissa", desc=True) \
        .limit(limit) \
        .execute()

    return res.data
if __name__ == "__main__":

    account = get_account("Wizard10989")
    print(account)

    top = get_top_cash()

    print("\nLeaderboard:")
    for row in top:
        print(row)