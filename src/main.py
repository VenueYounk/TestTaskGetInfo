import disnake
from vk_helper import VkDataExtractor, errors

from disnake.ext import commands


import os


TOKEN = os.getenv("DISCORD_BOT_TOKEN")


bot = commands.Bot(command_prefix="/", help_command=None, intents=disnake.Intents.all())


@bot.slash_command(name="get_info", description="/get_info <ссылка на страницу>")
async def get_vk_info(ctx, vk_link: str):
    await ctx.response.defer()

    try:
        vk_page = VkDataExtractor(vk_link)
    except errors.PageNotFound:
        await ctx.send("Страница не существует")
        return
    except errors.InvalidLink:
        await ctx.send("Ссылка не валидна")
        return
    except Exception as e:
        print(e)
        await ctx.send(f"Произошла неожиданная ошибка")
        return

    description = (
        f"Тип: {'Группа' if vk_page.page_type == 'group' else 'Пользователь'}\n"
        f"Имя: {vk_page.name}\n"
        f"ID: {vk_page.id}\n"
    )
    if hasattr(vk_page, "created_date"):
        description += f"\nДата создания: {vk_page.created_date}"

    embed = disnake.Embed(title="Информация о странице", description=description)
    embed.set_image(url=vk_page.photo)
    await ctx.send(embed=embed)


bot.run(TOKEN)
