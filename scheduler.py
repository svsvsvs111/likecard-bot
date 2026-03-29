import asyncio
from database import get_subscriptions, deactivate_subscription
from likecard_api import check_product, create_order, get_order_details
from config import CHECK_INTERVAL

async def checker(bot):
    while True:
        subs = get_subscriptions()

        for sub in subs:
            sub_id, user_id, product_id, product_name, _ = sub

            if check_product(product_id):
                order_id = create_order(product_id)

                if order_id:
                    await asyncio.sleep(5)

                    code = get_order_details(order_id)

                    if code:
                        await bot.send_message(
                            chat_id=user_id,
                            text=f"✅ تم شراء {product_name}\\n🎁 الكود:\\n{code}"
                        )

                        deactivate_subscription(sub_id)

        await asyncio.sleep(CHECK_INTERVAL)
