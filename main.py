from Capstone.scraper import scrapehtml, scrape_website, check_matches, webscrape
from user_control import register_user, login_user
def main():
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option (1-3): ")
        match choice:
            case "1":
                register_user()
                continue
            case "2":
                if login_user():
                    while True:
                        print("\n1. Scraping")
                        print("2. Exit")
                        choice = input("Choose an option (1-2): ")
                        match choice:
                            case "1":
                                while True:
                                    print("\n1. HTML Scraping")
                                    print("2. Web Scraping")
                                    print("3. Back")
                                    choice = input("Choose an option (1-3): ")
                                    match choice:
                                        case "1":
                                            usernames, emails = scrapehtml(input("Enter Filename(without extension): "))
                                            check_matches(usernames, emails)
                                        case "2":
                                            usernames, emails = scrape_website(input("Enter Full URL: "))
                                            print(emails)
                                            check_matches(usernames, emails)
                                        case "3":
                                            print("Goodbye!")
                                            break
                                        case _:
                                            print("Invalid choice, try again.")
                            case "2":
                                print("Goodbye!")
                                break
                            case _:
                                print("Invalid choice, try again.")
                                continue
            case "3":
                print("Goodbye!")
                break
            case _:
                print("Invalid choice, try again.")
                continue




if __name__ == "__main__":
    main()
