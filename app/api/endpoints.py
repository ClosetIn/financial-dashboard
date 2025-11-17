import logging
from datetime import datetime
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException

from app.core.config import Settings, get_settings
from app.services.cbr_service import cbr_service

# Настраиваем логирование
logger = logging.getLogger(__name__)

# Создаем роутер
router = APIRouter(tags=["financial-data"])


@router.get("/rates/cbr", summary="Get CBR currency rates")
async def get_cbr_rates(settings: Settings = Depends(get_settings)) -> Dict:
    """
    Получает актуальные курсы валют от Центрального Банка России.

    Returns:
        Dict: Курсы валют и метаданные
    """
    try:
        logger.info("Fetching CBR rates")

        rates = await cbr_service.get_rates()

        response_data = {
            "source": "cbr",
            "data": {
                currency: {
                    "currency": rate.currency,
                    "rate": rate.rate,
                    "change": rate.change,
                    "change_percent": rate.change_percent,
                    "timestamp": rate.timestamp.isoformat(),
                }
                for currency, rate in rates.items()
            },
            "timestamp": datetime.now().isoformat(),
            "currencies_count": len(rates),
            "success": True,
        }

        logger.info(f"Successfully returned rates for {len(rates)} currencies")
        return response_data
    except Exception as e:
        logger.error(f"Error in CBR rates endpoint: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch CBR rates: {str(e)}"
        )


@router.get("/rates/cbr/{currency}", summary="Get specific CBR currency rate")
async def get_specific_cbr_rate(
    currency: str, settings: Settings = Depends(get_settings)
) -> Dict:
    """
    Получает курс конкретной валюты от ЦБ РФ.

    Args:
        currency: Код валюты (USD, EUR, CNY, etc.)

    Returns:
        Dict: Данные по конкретной валюте
    """
    try:
        logger.info(f"Fetching CBR rate for {currency}")

        rate = await cbr_service.get_specific_rate(currency.upper())

        if not rate:
            raise HTTPException(
                status_code=404,
                detail=f"Currency {currency} not found or not supported",
            )

        response_data = {
            "source": "cbr",
            "data": {
                "currency": rate.currency,
                "rate": rate.rate,
                "change": rate.change,
                "change_percent": rate.change_percent,
                "timestamp": rate.timestamp.isoformat(),
            },
            "timestamp": datetime.now().isoformat(),
            "success": True,
        }

        logger.info(f"Successfully returned rate for {currency}")
        return response_data

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching rate for {currency}: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch rate for {currency}: {str(e)}"
        )


@router.get("/currencies/supported", summary="Get supported currencies")
async def get_supported_currencies() -> Dict:
    """
    Возвращает список поддерживаемых валют.

    Returns:
        Dict: Список поддерживаемых валют
    """
    return {
        "supported_currencies": cbr_service.tracked_currencies,
        "count": len(cbr_service.tracked_currencies),
    }
