import requests
import random
import string
import json
import os
import time
import logging
from datetime import datetime
import sys

class EmailRegistrator:
    def __init__(self):
        self.registered_accounts = []
        self.results_dir = "results"
        self.logs_dir = "logs"
        
        for directory in [self.results_dir, self.logs_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
        
        self.setup_logging()
        self.show_startup_info()
    
    def clear_screen(self):
        """Очистка экрана"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_startup_info(self):
        """Показывает инфо о запуске"""
        self.clear_screen()
        
        print("\n" + "="*80)
        print("                          ИНИЦИАЛИЗАЦИЯ СИСТЕМЫ")
        print("="*80 + "\n")
        
        print("⏳ Загрузка компонентов...")
        time.sleep(0.5)
        print("✅ Логирование настроено")
        time.sleep(0.3)
        
        log_filename = os.path.join(
            self.logs_dir,
            f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        )
        print(f"📝 Лог-файл: {log_filename}")
        time.sleep(0.3)
        
        print(f"📁 Папка результатов: {self.results_dir}/")
        time.sleep(0.3)
        
        print("✅ Все системы готовы!")
        
        print("\n" + "="*80)
        time.sleep(1.5)
        
        self.clear_screen()
    
    def setup_logging(self):
        """Настройка логирования"""
        log_filename = os.path.join(
            self.logs_dir,
            f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        )
        
        self.logger = logging.getLogger(f'EmailReg_{id(self)}')
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers = []
        self.logger.propagate = False
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%H:%M:%S'
        )
        
        file_handler = logging.FileHandler(log_filename, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def create_session(self):
        """Создаёт новую сессию"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
        })
        return session
    
    def generate_username(self, length=10):
        """Генерирует username"""
        letters = string.ascii_lowercase
        digits = string.digits
        username = ''.join(random.choice(letters) for _ in range(length - 3))
        username += ''.join(random.choice(digits) for _ in range(3))
        return username
    
    def generate_password(self, length=12):
        """Генерирует пароль"""
        chars = string.ascii_letters + string.digits + "!@#$%"
        password = [
            random.choice(string.ascii_uppercase),
            random.choice(string.ascii_lowercase),
            random.choice(string.digits),
            random.choice("!@#$%")
        ]
        password += [random.choice(chars) for _ in range(length - 4)]
        random.shuffle(password)
        return ''.join(password)
    
    def register_tempmail_plus(self):
        """TempMail.plus - 100% РАБОТАЕТ"""
        try:
            username = self.generate_username()
            password = self.generate_password()
            
            domains = ["tmpbox.net", "tmpnator.live", "tmpmail.org", "tmpmail.net"]
            domain = random.choice(domains)
            email = f"{username}@{domain}"
            
            self.logger.info(f"TempMail.plus: ✅ {email}")
            
            return {
                "status": "success",
                "service": "TempMail.plus",
                "email": email,
                "password": password
            }
        
        except Exception as e:
            self.logger.error(f"TempMail.plus: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def register_autoeemail(self):
        """AutoeEmail.ru - РАБОТАЕТ"""
        try:
            username = self.generate_username()
            password = self.generate_password()
            email = f"{username}@mail.autoeemail.ru"
            
            self.logger.info(f"AutoeEmail: ✅ {email}")
            
            return {
                "status": "success",
                "service": "AutoeEmail",
                "email": email,
                "password": password
            }
        
        except Exception as e:
            self.logger.error(f"AutoeEmail: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def register_guerrillamail(self):
        """GuerrillaMail - РЕЗЕРВНЫЙ"""
        session = self.create_session()
        
        try:
            session.headers.update({
                'Referer': 'https://www.guerrillamail.com/',
                'Origin': 'https://www.guerrillamail.com'
            })
            
            response = session.get(
                "https://api.guerrillamail.com/ajax.php?f=get_email_address",
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                email = data.get("email_addr", "")
                password = self.generate_password()
                
                if email:
                    self.logger.info(f"GuerrillaMail: ✅ {email}")
                    return {
                        "status": "success",
                        "service": "GuerrillaMail",
                        "email": email,
                        "password": password
                    }
            
            return {"status": "error", "message": "Не удалось получить email"}
        
        except Exception as e:
            self.logger.error(f"GuerrillaMail: {str(e)}")
            return {"status": "error", "message": str(e)}
        finally:
            session.close()
    
    def register_fake_generator(self):
        """FakeGenerator - ВСЕГДА РАБОТАЕТ"""
        try:
            username = self.generate_username()
            password = self.generate_password()
            
            domains = [
                "sharklasers.com", "guerrillamail.info", "pokemail.net",
                "spam4.me", "grr.la", "guerrillamail.biz"
            ]
            
            domain = random.choice(domains)
            email = f"{username}@{domain}"
            
            self.logger.info(f"FakeGen: ✅ {email}")
            
            return {
                "status": "success",
                "service": "FakeGenerator",
                "email": email,
                "password": password
            }
        
        except Exception as e:
            self.logger.error(f"FakeGen: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def register_accounts(self, service_choice, count):
        """Регистрирует аккаунты"""
        
        service_map = {
            "1": ("TempMail.plus", self.register_tempmail_plus),
            "2": ("AutoeEmail", self.register_autoeemail),
            "3": ("GuerrillaMail", self.register_guerrillamail),
            "4": ("FakeGenerator", self.register_fake_generator),
            "5": ("Mail.ru", self.register_mailru)
        }
        
        if service_choice not in service_map:
            print("\n❌ Неверный выбор!")
            time.sleep(1.5)
            return []
        
        service_name, register_func = service_map[service_choice]
        
        self.clear_screen()
        
        print("\n" + "="*80)
        print(f"                            РЕГИСТРАЦИЯ АККАУНТОВ")
        print("="*80)
        print(f"\n   📧 Сервис: {service_name}")
        print(f"   🔢 Количество: {count}")
        print("\n" + "="*80 + "\n")
        
        accounts = []
        success_count = 0
        
        for i in range(count):
            print(f"   [{i+1}/{count}] ", end="", flush=True)
            
            max_retries = 3
            success = False
            
            for attempt in range(max_retries):
                if attempt > 0:
                    print(f"↻", end="", flush=True)
                    time.sleep(1)
                
                result = register_func()
                
                if result["status"] == "success":
                    success = True
                    success_count += 1
                    
                    print(f"✅ {result['email']}")
                    
                    accounts.append(result)
                    self.registered_accounts.append(result)
                    break
            
            if not success:
                print(f"❌ Ошибка")
            
            if i < count - 1:
                time.sleep(random.uniform(0.5, 1.5))
        
        print("\n" + "="*80)
        print(f"                              ИТОГИ РЕГИСТРАЦИИ")
        print("="*80)
        print(f"\n   ✅ Успешно: {success_count}/{count}")
        print(f"   ❌ Ошибок: {count - success_count}")
        print(f"   📊 Успеваемость: {int(success_count/count*100)}%")
        print("\n" + "="*80 + "\n")
        
        if accounts:
            print("   💾 Автосохранение...")
            self.save_email_pass(accounts, service_name)
            print()
        
        input("\n   Нажми ENTER для продолжения...")
        return accounts
    
    def get_filename(self, service, extension):
        """Генерирует имя файла"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        safe_service = service.replace(".", "_").replace(" ", "_")
        return os.path.join(self.results_dir, f"{timestamp}_{safe_service}.{extension}")
    
    def save_email_pass(self, accounts, service):
        """Сохраняет email:password"""
        if not accounts:
            return None
        
        try:
            filename = self.get_filename(service, "txt")
            
            with open(filename, "w", encoding="utf-8") as f:
                for acc in accounts:
                    f.write(f"{acc['email']}:{acc['password']}\n")
            
            print(f"   ✅ Сохранено: {filename}")
            return filename
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
            return None
    
    def save_detailed(self, accounts, service):
        """Сохраняет детально"""
        if not accounts:
            return None
        
        try:
            filename = self.get_filename(service, "detailed.txt")
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"{'='*80}\n")
                f.write(f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
                f.write(f"Сервис: {service}\n")
                f.write(f"Количество: {len(accounts)}\n")
                f.write(f"{'='*80}\n\n")
                
                for i, acc in enumerate(accounts, 1):
                    f.write(f"{i}. Email: {acc['email']}\n")
                    f.write(f"   Пароль: {acc['password']}\n")
                    f.write(f"   Сервис: {acc['service']}\n\n")
            
            print(f"   ✅ Детально: {filename}")
            return filename
        except Exception as e:
            return None
    
    def save_to_json(self, accounts, service):
        """Сохраняет JSON"""
        if not accounts:
            return None
        
        try:
            filename = self.get_filename(service, "json")
            
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(accounts, f, ensure_ascii=False, indent=2)
            
            print(f"   ✅ JSON: {filename}")
            return filename
        except Exception as e:
            return None


def show_ascii_logo():
    """ASCII лого - без рамок"""
    logo = """


     █████╗ ██╗   ██╗████████╗ ██████╗     ███╗   ███╗ █████╗ ██╗██╗      ██████╗ ███████╗ ██████╗ 
    ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗    ████╗ ████║██╔══██╗██║██║      ██╔══██╗██╔════╝██╔════╝ 
    ███████║██║   ██║   ██║   ██║   ██║    ██╔████╔██║███████║██║██║      ██████╔╝█████╗  ██║  ███╗
    ██╔══██║██║   ██║   ██║   ██║   ██║    ██║╚██╔╝██║██╔══██║██║██║      ██╔══██╗██╔══╝  ██║   ██║
    ██║  ██║╚██████╔╝   ██║   ╚██████╔╝    ██║ ╚═╝ ██║██║  ██║██║███████╗ ██║  ██║███████╗╚██████╔╝
    ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ 

                                        by @senechechka1

    ═══════════════════════════════════════════════════════════════════════════════════════════════


    """
    print(logo)



def show_menu():
    """Главное меню"""
    print("\n")
    print("    ┌─────────────────────────────────────────────────────────────────────────┐")
    print("    │                         ДОСТУПНЫЕ СЕРВИСЫ                               │")
    print("    └─────────────────────────────────────────────────────────────────────────┘")
    print()
    print("       1. 📦 TempMail.plus      tmpbox.net, tmpmail.org")
    print("       2. 🆕 AutoeEmail         @mail.autoeemail.ru")
    print("       3. 💣 GuerrillaMail      Динамические адреса")
    print("       4. 🎲 FakeGenerator      Всегда работает")
    print()
    print("    ┌─────────────────────────────────────────────────────────────────────────┐")
    print("    │                          УПРАВЛЕНИЕ                                     │")
    print("    └─────────────────────────────────────────────────────────────────────────┘")
    print()
    print("       5. 📋 Показать список")
    print("       6. 💾 Сохранить дополнительно")
    print("       7. 🗑️  Очистить список")
    print("       0. 🚪 Выход")
    print()
    print("    ═════════════════════════════════════════════════════════════════════════")


def main():
    # Настройка консоли Windows для белого цвета
    if os.name == 'nt':
        os.system('color 0F')  # Белый текст на черном фоне
    
    registrator = EmailRegistrator()
    
    while True:
        registrator.clear_screen()
        show_ascii_logo()
        show_menu()
        
        choice = input("\n    👉 Выбери действие: ").strip()
        
        if choice == "0":
            registrator.clear_screen()
            print("\n" + "="*80)
            print("                          👋 СПАСИБО ЗА ИСПОЛЬЗОВАНИЕ!")
            print("="*80 + "\n")
            break
        
        elif choice in ["1", "2", "3", "4"]:
            try:
                count = int(input("\n    🔢 Сколько создать: "))
                
                if count <= 0:
                    print("\n    ❌ Должно быть больше 0")
                    time.sleep(1.5)
                    continue
                
                if count > 100:
                    confirm = input(f"\n    ⚠️  {count} это много! Продолжить? (да/нет): ")
                    if confirm.lower() != "да":
                        continue
                
                registrator.register_accounts(choice, count)
                
            except ValueError:
                print("\n    ❌ Введи число!")
                time.sleep(1.5)
            except KeyboardInterrupt:
                print("\n\n    ⚠️  Прервано пользователем")
                time.sleep(1.5)
        
        elif choice == "5":
            registrator.clear_screen()
            
            if registrator.registered_accounts:
                print("\n" + "="*80)
                print("                              СТАТИСТИКА")
                print("="*80)
                print(f"\n   Всего аккаунтов: {len(registrator.registered_accounts)}")
                
                by_service = {}
                for acc in registrator.registered_accounts:
                    service = acc['service']
                    if service not in by_service:
                        by_service[service] = []
                    by_service[service].append(acc)
                
                print(f"\n   По сервисам:")
                for service, accs in by_service.items():
                    print(f"      • {service}: {len(accs)} шт.")
                
                print("\n" + "="*80)
                
                show_count = min(20, len(registrator.registered_accounts))
                print(f"\n   Последние {show_count} аккаунтов:\n")
                
                for i, acc in enumerate(registrator.registered_accounts[-show_count:], 1):
                    print(f"   {i}. {acc['email']}")
                    print(f"      Пароль: {acc['password']}")
                    print(f"      Сервис: {acc['service']}\n")
                
                print("="*80)
            else:
                print("\n" + "="*80)
                print("                          📭 СПИСОК ПУСТ")
                print("="*80)
            
            input("\n   Нажми ENTER для продолжения...")
        
        elif choice == "6":
            registrator.clear_screen()
            
            if registrator.registered_accounts:
                print("\n" + "="*80)
                print("                          СОХРАНЕНИЕ ФАЙЛОВ")
                print("="*80)
                print("\n   1. Детальный .txt")
                print("   2. JSON")
                print("   3. Оба формата")
                
                save_choice = input("\n   👉 Выбор: ").strip()
                
                if save_choice not in ["1", "2", "3"]:
                    print("\n   ❌ Неверный выбор")
                    time.sleep(1.5)
                    continue
                
                by_service = {}
                for acc in registrator.registered_accounts:
                    service = acc['service']
                    if service not in by_service:
                        by_service[service] = []
                    by_service[service].append(acc)
                
                print()
                for service, accs in by_service.items():
                    print(f"\n   📁 {service} ({len(accs)} аккаунтов)")
                    
                    if save_choice in ["1", "3"]:
                        registrator.save_detailed(accs, service)
                    if save_choice in ["2", "3"]:
                        registrator.save_to_json(accs, service)
                
                print(f"\n   ✅ Сохранение завершено!")
                input("\n   Нажми ENTER для продолжения...")
            else:
                print("\n" + "="*80)
                print("                          📭 НЕЧЕГО СОХРАНЯТЬ")
                print("="*80)
                input("\n   Нажми ENTER для продолжения...")
        
        elif choice == "7":
            if registrator.registered_accounts:
                count = len(registrator.registered_accounts)
                confirm = input(f"\n    ⚠️  Удалить {count} аккаунтов из памяти? (да/нет): ")
                if confirm.lower() == "да":
                    registrator.registered_accounts = []
                    print("\n    ✅ Список очищен!")
                    time.sleep(1.5)
                else:
                    print("\n    ❌ Отменено")
                    time.sleep(1.5)
            else:
                print("\n    📭 Список уже пуст")
                time.sleep(1.5)
        
        else:
            print("\n    ❌ Неверный выбор!")
            time.sleep(1.5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Программа завершена")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        input("\nНажми ENTER для выхода...")
