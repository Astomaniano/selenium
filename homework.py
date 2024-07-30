from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_paragraphs(browser):
    """Выводит текст параграфов текущей страницы и позволяет перейти к ссылкам или завершить программу"""
    paragraphs = browser.find_elements(By.TAG_NAME, "p")
    for paragraph in paragraphs:
        print(paragraph.text)
        user_choice = input("Нажмите Enter, чтобы продолжить к следующему параграфу,\n"
                            "введите 'ссылки', чтобы посмотреть доступные ссылки,\n"
                            "или 'выход', чтобы завершить программу: ").strip().lower()

        if user_choice == '':
            continue
        elif user_choice == 'ссылки':
            return 'ссылки'
        elif user_choice == 'выход':
            return 'выход'
    print("Конец параграфов.")
    return 'продолжить'


def get_links(browser):
    """Возвращает список ссылок на текущей странице"""
    links = browser.find_elements(By.XPATH, "//a[@href]")
    link_texts = [link.text for link in links if link.text]
    link_hrefs = [link.get_attribute('href') for link in links if link.text]
    return list(zip(link_texts, link_hrefs))


def main():
    browser = webdriver.Chrome()
    try:
        browser.get(
            "https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")

        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "searchInput")))

        user_input = input('Что вы хотите найти? ')
        search_box = browser.find_element(By.ID, "searchInput")
        search_box.send_keys(user_input)
        search_box.send_keys(Keys.RETURN)

        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "firstHeading")))

        while True:
            user_choice = input('Чтобы продолжить изучение темы нажмите "Enter",\n'
                                'чтобы посмотреть доступные ссылки введите "ссылки",\n'
                                'чтобы выйти из программы введите "выход": ').strip().lower()
            if user_choice == '':
                result = get_paragraphs(browser)
                if result == 'ссылки':
                    user_choice = 'ссылки'
                elif result == 'выход':
                    break
                else:
                    continue
            if user_choice == 'ссылки':
                links = get_links(browser)
                if not links:
                    print("Ссылки не найдены.")
                    continue
                for i, (text, href) in enumerate(links):
                    print(f"{i + 1}. {text}")
                link_choice = input("Введите номер ссылки, чтобы перейти по ней, или 'назад' для возврата: ").strip().lower()
                if link_choice == 'назад':
                    continue
                try:
                    link_index = int(link_choice) - 1
                    if 0 <= link_index < len(links):
                        browser.get(links[link_index][1])
                        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "firstHeading")))
                    else:
                        print("Некорректный номер ссылки.")
                except ValueError:
                    print("Некорректный ввод.")
            elif user_choice == 'выход':
                break
            else:
                print("Некорректный выбор. Пожалуйста, попробуйте снова.")
    finally:
        browser.quit()


if __name__ == "__main__":
    main()