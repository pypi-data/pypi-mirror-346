# yandex_aiobot_py



## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/topics/git/add_files/#add-files-to-a-git-repository) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.com/demkinkv/yandex_aiobot_py.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://gitlab.com/demkinkv/yandex_aiobot_py/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/user/project/merge_requests/auto_merge/)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

```
import asyncio
import logging
from yandex_aiobot_py.client import Client, Button, Message
from config import API_KEY

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def main():
    bot = Client(api_key=API_KEY)

    @bot.on_message("/start", chat_type="group")
    async def start_handler_g(message: Message):
        await bot.send_message(
            text="Вы обратились ко мне из группы!",
            chat_id=message.chat.chat_id,
        )

    @bot.on_message("/start", chat_type="private")
    async def start_handler_p(message: Message):
        await bot.send_message(
            text="Это личный чат.",
            login=message.user.login,
        )

    @bot.on_message("/image", chat_type="private")
    async def image_handler_p(message: Message):
        await bot.send_image(
            "/data/Script/Python/MyLibrary/yandex_aiobot_py/files/5435871924950525925.jpg",
            login=message.user.login,
        )

    @bot.on_message("/start")
    async def start_handler(message: Message):
        if message.chat and message.chat.chat_id:
            await bot.send_message(
                text="!!Вы обратились ко мне из группы!!!!",
                chat_id=message.chat.chat_id,
            )
        else:
            await bot.send_message(
                text="Это личный чат. 1",
                login=message.user.login,
            )

    @bot.on_message(r"/menu")
    async def show_menu(message: Message):
        btn = [
            Button(
                text="Выход",
                phrase="/exit_poll",
                callback_data={"actions": "exit_poll"},
            )
        ]

        await bot.send_message(
            text="Отправьте ссылку на чат",
            login=message.user.login,
            inline_keyboard=btn,
        )

    @bot.on_message(r".*")
    async def echo_handler(message: Message):
        chat_id = getattr(message.chat, "chat_id", None)
        logger.debug(f"Message chat_id: {chat_id}")
        logger.debug(f"Message user login: {message.user.login}")

        try:
            if chat_id:
                # Отправляем в чат, если chat_id есть
                await bot.send_message(
                    text=f"Вы написали: {message.text}", chat_id=chat_id
                )
            elif message.user and message.user.login:
                # Если chat_id нет, отправляем по логину пользователя
                await bot.send_message(
                    text=f"Вы написали: {message.text}", login=message.user.login
                )
            else:
                logger.warning(
                    f"Не удалось определить chat_id или login для сообщения: {message}"
                )
        except Exception as e1:
            logger.exception(f"Ошибка при обработке сообщения: {e1}")

    try:
        await bot.start_session()
        await bot.run()  # Запускаем метод run с асинхронным polling и watchdog
    except asyncio.CancelledError:
        logger.info("Bot stopped by cancellation")
    except Exception as e2:
        logger.exception(f"Произошла ошибка при запуске бота: {e2}")
    finally:
        await bot.close_session()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Программа остановлена пользователем")
```

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
