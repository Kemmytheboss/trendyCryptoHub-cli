import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers import (
    show_main_menu,
    create_user_flow,
    list_users_flow,
    backtest_flow,
    get_deposit_address_flow,
    request_withdrawal_flow,
    approve_withdrawal_flow,
    list_transactions_flow,
    make_admin_flow
)


def main():
    print("Welcome to TrendyCryptoHub CLI!")

    while True:
        show_main_menu()
        choice = input("> ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        elif choice == "1":
            create_user_flow()

        elif choice == "2":
            list_users_flow()

        elif choice == "3":
            backtest_flow()

        elif choice == "4":
            get_deposit_address_flow()

        elif choice == "5":
            request_withdrawal_flow()

        elif choice == "6":
            approve_withdrawal_flow()

        elif choice == "7":
            list_transactions_flow()

        elif choice == "8":
            make_admin_flow()

        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
