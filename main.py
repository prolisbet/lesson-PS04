from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

import time
import random
import pprint

browser = webdriver.Chrome()
browser.get("https://ru.wikipedia.org/wiki/")

assert "Википедия" in browser.title

try:
    first_search = str(input('Введите ваш запрос: '))
    search_box = browser.find_element(By.ID, "searchInput")
    search_box.send_keys(first_search)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)

    # Проверка, что выбор будет ссылкой на Википедии, а не в Викисловаре, например.
    # Класс основной колонки с результатами:
    main_container = browser.find_element(By.CLASS_NAME, "mw-search-results-container")
    page = main_container.find_element(By.TAG_NAME, "a")
    page.click()

    assert "Википедия" in browser.title

    browsing = True

    while browsing:
        try:
            next_step = input('\n    Выберите действие:\n'
                              '1. Листать параграфы текущей статьи\n'
                              '2. Перейти на одну из связанных страниц\n'
                              '3. Выйти из программы\n'
                              '    Введите цифру 1/2/3: ').strip()

            next_step = int(next_step)

            if next_step == 3:
                browsing = False

            elif next_step == 2:
                try:
                    hatnotes = []
                    for element in browser.find_elements(By.TAG_NAME, "div"):
                        cl = element.get_attribute("class")
                        if cl == "hatnote navigation-not-searchable":
                            hatnote = element.find_element(By.TAG_NAME, "a")
                            href = hatnote.get_attribute("href")
                            class_name = hatnote.get_attribute("class")

                            # Проверка, что страница существует
                            if class_name != "new":
                                hatnotes.append(href)

                    link = random.choice(hatnotes)
                    browser.get(link)

                except:
                    print("Связанные основные статьи не найдены. Выбираем любую ссылку на странице")

                    # Получение всех ссылок на странице
                    all_links = browser.find_elements(By.TAG_NAME, "a")

                    # Фильтрация ссылок
                    article_links = []
                    for link in all_links:
                        href = link.get_attribute("href")
                        class_name = link.get_attribute("class")

                        if href and class_name == "mv-redirect":
                            article_links.append(href)

                        # Проверка, что ссылка ведет на другую статью и не является ссылкой на примечания
                        # или другие неподходящие ссылки
                        if href and not class_name:
                            if href.startswith("https://ru.wikipedia.org/wiki/") and "Служебная:" not in href:
                                article_links.append(href)

                    link = random.choice(article_links)
                    browser.get(link)

            elif next_step == 1:
                try:
                    paragraphs = browser.find_elements(By.TAG_NAME, "p")
                    for paragraph in paragraphs:
                        pprint.pprint(paragraph.text)
                        par_choice = input("\n    Дальше? д/н: ").strip().lower()
                        if par_choice == "н":
                            raise StopIteration
                        else:
                            continue
                except StopIteration:
                    pass

            else:
                print('Вы ввели неподходящее значение')
                continue

        except ValueError:
            print('Вы ввели неподходящее значение')
            continue

        except KeyboardInterrupt:
            print('\nПрограмма прервана пользователем.')
            break

        except Exception as e:
            print(f'Произошла ошибка: {e}')
            continue

except:
    print("По вашему запросу ничего не найдено. Попробуйте снова")

finally:
    browser.quit()
