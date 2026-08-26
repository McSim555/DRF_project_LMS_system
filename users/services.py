import os

from stripe import StripeClient

client = StripeClient(os.getenv("STRIPE_API_KEY"))


def create_stripe_product(name, description=""):
    """Создаёт продукт в Stripe."""
    return client.v1.products.create(
        {
            "name": name,
            "description": description,
        }
    )


def create_stripe_price(product_id, amount):
    """Создаёт цену для продукта в Stripe."""
    return client.v1.prices.create(
        {
            "currency": "rub",
            "unit_amount": int(amount * 100),
            "product": product_id,
        }
    )


def create_stripe_session(
    price,
    success_url="http://127.0.0.1:8000/",
):
    """Создаёт сессию оплаты и возвращает (session_id, session_url)."""
    session = client.v1.checkout.sessions.create(
        {
            "success_url": success_url,
            "line_items": [{"price": price, "quantity": 1}],
            "mode": "payment",
        }
    )
    return session.id, session.url, session.amount_total
