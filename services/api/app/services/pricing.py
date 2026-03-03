"""
Purchasing Power Parity (PPP) Pricing Engine
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class LocalizedPrice:
    """Localized price with currency info"""
    country_code: str
    plan: str
    base_price_usd: float
    ppp_ratio: float
    display_price_usd: float
    local_currency: str
    local_symbol: str
    local_amount: int
    razorpay_amount: int  # Smallest currency unit


# PPP ratios - lower means cheaper for that country
PPP_RATIOS = {
    # Premium markets
    "US": 1.0, "GB": 1.0, "CA": 1.0, "AU": 1.0, "JP": 1.0,
    "DE": 1.0, "FR": 1.0, "NL": 1.0, "SE": 1.0, "CH": 1.0, "SG": 1.0, "KR": 0.9,
    
    # Emerging markets (discounted)
    "IN": 0.25, "ID": 0.30, "PH": 0.35, "VN": 0.30, "TH": 0.35, "MY": 0.40,
    "BR": 0.35, "MX": 0.45, "AR": 0.30, "CO": 0.35, "CL": 0.40,
    "ZA": 0.35, "NG": 0.20, "EG": 0.25, "KE": 0.25, "GH": 0.25,
    "PK": 0.25, "BD": 0.25, "LK": 0.30, "NP": 0.25,
    
    "DEFAULT": 0.40,
}


# Currency configuration
CURRENCY_CONFIG = {
    "US": {"currency": "USD", "symbol": "$", "multiplier": 100},
    "IN": {"currency": "INR", "symbol": "₹", "multiplier": 100},
    "BR": {"currency": "BRL", "symbol": "R$", "multiplier": 100},
    "ID": {"currency": "IDR", "symbol": "Rp", "multiplier": 1},
    "PH": {"currency": "PHP", "symbol": "₱", "multiplier": 100},
    "VN": {"currency": "VND", "symbol": "₫", "multiplier": 1},
    "TH": {"currency": "THB", "symbol": "฿", "multiplier": 100},
    "MX": {"currency": "MXN", "symbol": "Mex$", "multiplier": 100},
    "NG": {"currency": "NGN", "symbol": "₦", "multiplier": 100},
    "EG": {"currency": "EGP", "symbol": "E£", "multiplier": 100},
    "PK": {"currency": "PKR", "symbol": "₨", "multiplier": 100},
    "BD": {"currency": "BDT", "symbol": "৳", "multiplier": 100},
    "LK": {"currency": "LKR", "symbol": "Rs", "multiplier": 100},
    "ZA": {"currency": "ZAR", "symbol": "R", "multiplier": 100},
    "MY": {"currency": "MYR", "symbol": "RM", "multiplier": 100},
    "DEFAULT": {"currency": "USD", "symbol": "$", "multiplier": 100},
}


# Plan configurations
PLAN_CONFIGS = {
    "free": {
        "base_price": 0,
        "anime_videos": 3,
        "realistic_videos": 1,
        "features": ["watermark", "720p", "community_support"],
    },
    "starter": {
        "base_price": 9.99,
        "anime_videos": 15,
        "realistic_videos": 5,
        "features": ["no_watermark", "1080p", "basic_support"],
    },
    "creator": {
        "base_price": 29.99,
        "anime_videos": 50,
        "realistic_videos": 20,
        "features": ["priority_generation", "auto_posting", "email_support"],
    },
    "pro": {
        "base_price": 79.99,
        "anime_videos": 150,
        "realistic_videos": 60,
        "features": ["4k", "voice_cloning", "analytics", "priority_support"],
    },
    "agency": {
        "base_price": 199.99,
        "anime_videos": 500,
        "realistic_videos": 200,
        "features": ["api_access", "white_label", "dedicated_manager"],
    },
}


def get_localized_price(country_code: str, plan: str) -> LocalizedPrice:
    """Calculate PPP-adjusted price for a country and plan"""
    base_price = PLAN_CONFIGS[plan]["base_price"]
    ppp_ratio = PPP_RATIOS.get(country_code, PPP_RATIOS["DEFAULT"])
    
    if base_price == 0:
        adjusted_price = 0
    else:
        adjusted_price = base_price * ppp_ratio
    
    # Psychological pricing
    if adjusted_price > 0:
        if adjusted_price < 5:
            display_price = round(adjusted_price * 0.95, 2)
        else:
            display_price = int(adjusted_price) - 0.01
    else:
        display_price = 0
    
    currency_config = CURRENCY_CONFIG.get(country_code, CURRENCY_CONFIG["DEFAULT"])
    local_amount = int(display_price * currency_config["multiplier"])
    
    return LocalizedPrice(
        country_code=country_code,
        plan=plan,
        base_price_usd=base_price,
        ppp_ratio=ppp_ratio,
        display_price_usd=display_price,
        local_currency=currency_config["currency"],
        local_symbol=currency_config["symbol"],
        local_amount=local_amount,
        razorpay_amount=local_amount,
    )


def get_plan_limits(plan: str) -> Dict:
    """Get video limits for a plan"""
    config = PLAN_CONFIGS.get(plan, PLAN_CONFIGS["free"])
    return {
        "anime_videos": config["anime_videos"],
        "realistic_videos": config["realistic_videos"],
        "features": config["features"],
    }


def get_all_prices_for_country(country_code: str) -> Dict[str, LocalizedPrice]:
    """Get all plan prices for a country"""
    return {
        plan: get_localized_price(country_code, plan)
        for plan in PLAN_CONFIGS.keys()
    }