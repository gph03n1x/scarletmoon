from core.getch import getch
import os

def clear_console():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")


def show_results(results, message=None, menu=True):
    clear_console()
    for result in results:
        print("[*] Article :" + result[0]["article"].strip())
        print("    Document:" + result[0]["document"].strip())
        print("    tf-idf  : " + str(result[1]))

    if menu:
        print("[*] Type [n] for next results ")
        print("[*] >>>> [p] for previous results")
        print("[*] >>>> [q] to leave results")

        if message is not None:
            print(message)


def results_menu(results):

    results_per_page = 5
    point = 0
    results_number = len(results)
    message = None

    if results_number <= results_per_page:
        show_results(results[point:point+results_per_page], menu=False)
        return

    while results_number > results_per_page:

        show_results(results[point:point+results_per_page], message)

        try:
            choice = getch().decode("utf-8")
        except UnicodeDecodeError:
            choice = ""

        message = None
        if choice == "n":
            if point + results_per_page > results_number:
                message = "[-] There are no more results"
            else:
                point += results_per_page

        elif choice == "p":
            point -= results_per_page
            if point < 0:
                message = "[-] There are no previous results"
                point = 0

        elif choice == "q":
            break

        else:
            message = "[+] Invalid choice"
