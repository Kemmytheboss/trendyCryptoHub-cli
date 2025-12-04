from helpers import (
show_main_menu,
create_user_flow,
list_users_flow,
backtest_flow,
)




def main():
    print('Welcome to TrendyCryptoHub CLI')
    while True:
        show_main_menu()
        choice = input('> ').strip()
        if choice == '0':
            print('Goodbye!')
        break

        elif choice == '1':
            create_user_flow()
        elif choice == '2':
            list_users_flow()
        elif choice == '3':
            backtest_flow()
        else:
            print('Invalid choice')


if __name__ == '__main__':
main()