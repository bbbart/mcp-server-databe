import json
import os

import httpx
from mcp.server.fastmcp import FastMCP

BASE_URL = "https://api.data.be/2.0"

mcp = FastMCP(
    "data.be",
    instructions="Belgian company information from data.be",
)


def _get_api_key() -> str:
    key = os.environ.get("DATABE_API_KEY")
    if not key:
        raise ValueError(
            "DATABE_API_KEY environment variable is not set. "
            "Get your API key at https://data.be/en/api"
        )
    return key


def _headers() -> dict[str, str]:
    return {"x-data-api-key": _get_api_key()}


async def _get(path: str) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}{path}", headers=_headers(), timeout=30)
        resp.raise_for_status()
        return resp.json()


async def _post(path: str, body: dict) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{BASE_URL}{path}", headers=_headers(), json=body, timeout=30
        )
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def company_info(vat_number: str) -> str:
    """Get detailed company information for a Belgian company by VAT number.

    Returns company name, addresses, activities (NACE codes), juridical form,
    juridical situation, phone, email, website, establishment units, and more.

    Args:
        vat_number: European VAT number (e.g. "BE0844044609"). Should contain
            the country code and significant digits.
    """
    data = await _get(f"/companies/{vat_number}/info")
    return json.dumps(data, indent=2, ensure_ascii=False)


@mcp.tool()
async def financial_statements(vat_number: str) -> str:
    """Get financial statements (annual reports) for a Belgian company.

    Returns turnover, equity, employees, current assets, gross operating margin,
    tangible fixed assets, gain/loss, current ratio, net cash, return on equity,
    added value, and revisor information for each year.

    Args:
        vat_number: European VAT number (e.g. "BE0844044609").
    """
    data = await _get(f"/companies/{vat_number}/statements")
    return json.dumps(data, indent=2, ensure_ascii=False)


@mcp.tool()
async def legal_representative_persons(vat_number: str) -> str:
    """Get legal representative persons for a Belgian company.

    Returns full name, role code, associated company ID, and role dates
    for each person.

    Args:
        vat_number: European VAT number (e.g. "BE0844044609").
    """
    data = await _get(f"/companies/{vat_number}/legal_representative_persons")
    return json.dumps(data, indent=2, ensure_ascii=False)


@mcp.tool()
async def legal_representative_companies(vat_number: str) -> str:
    """Get legal representative companies for a Belgian company.

    Returns company name, role code, associated company ID, and role dates.

    Args:
        vat_number: European VAT number (e.g. "BE0844044609").
    """
    data = await _get(f"/companies/{vat_number}/legal_representative_companies")
    return json.dumps(data, indent=2, ensure_ascii=False)


@mcp.tool()
async def bank_accounts(vat_number: str) -> str:
    """Get all bank accounts for a Belgian company by VAT number.

    Returns IBAN, BIC, and start date for each account.

    Args:
        vat_number: European VAT number (e.g. "BE0844044609").
    """
    data = await _get(f"/companies/{vat_number}/bank_accounts")
    return json.dumps(data, indent=2, ensure_ascii=False)


@mcp.tool()
async def bank_account_check(vat_number: str, iban_number: str) -> str:
    """Check if a specific bank account belongs to a Belgian company.

    Args:
        vat_number: European VAT number (e.g. "BE0844044609").
        iban_number: Bank account number in IBAN format (e.g. "BE49735030379071").
    """
    data = await _get(f"/companies/{vat_number}/bank_accounts/{iban_number}")
    return json.dumps(data, indent=2, ensure_ascii=False)


@mcp.tool()
async def bank_account_lookup(iban_number: str) -> str:
    """Look up which company owns a given IBAN bank account number.

    Args:
        iban_number: Bank account number in IBAN format (e.g. "BE49735030379071").
    """
    data = await _get(f"/companies/bank_accounts/{iban_number}")
    return json.dumps(data, indent=2, ensure_ascii=False)


@mcp.tool()
async def stakeholders(vat_number: str) -> str:
    """Get stakeholders mentioned in a company's annual reports.

    Returns type, company name, person name, profession, address,
    mandate details for each stakeholder.

    Args:
        vat_number: European VAT number (e.g. "BE0844044609").
    """
    data = await _get(f"/companies/{vat_number}/stakeholders")
    return json.dumps(data, indent=2, ensure_ascii=False)


@mcp.tool()
async def vat_check(vat_number: str) -> str:
    """Validate a European VAT number via VIES (VAT Information Exchange System).

    Works for any EU country. Returns validity, company name and address.

    Args:
        vat_number: European VAT number (e.g. "BE0844044609").
    """
    data = await _get(f"/companies/{vat_number}/vies")
    return json.dumps(data, indent=2, ensure_ascii=False)


@mcp.tool()
async def company_guess(
    company_name: str | None = None,
    identifier: str | None = None,
    active: bool | None = None,
) -> str:
    """Guess/find a company by name and/or identifier.

    Lightweight search that returns basic company info. At least one of
    company_name or identifier should be provided.

    Args:
        company_name: Search query in company names.
        identifier: Search query in company identifiers.
        active: If true, search only active companies.
    """
    body: dict = {}
    if company_name is not None:
        body["company_name"] = company_name
    if identifier is not None:
        body["identifier"] = identifier
    if active is not None:
        body["active"] = str(active).lower()
    data = await _post("/companies/guess", body)
    return json.dumps(data, indent=2, ensure_ascii=False)


@mcp.tool()
async def company_search(
    q: str = "",
    active: bool | None = None,
    page: int = 1,
    max_results: int = 10,
    has_phone: bool | None = None,
    has_email: bool | None = None,
    has_website: bool | None = None,
    activity_codes: list[str] | None = None,
    juridical_form_codes: list[str] | None = None,
    zip_codes: list[str] | None = None,
    legal_person_types: list[str] | None = None,
    start_date_from: str | None = None,
    start_date_to: str | None = None,
    zip_code_from: str | None = None,
    zip_code_to: str | None = None,
) -> str:
    """Search for Belgian companies with filters.

    Warning: each company in the result costs one API credit. Use max_results=0
    first to get just the total count.

    Args:
        q: Free-text search query.
        active: If true, search only active companies.
        page: Page number (starts at 1).
        max_results: Max results per page (default 10).
        has_phone: Require at least one phone number.
        has_email: Require at least one email address.
        has_website: Require at least one website.
        activity_codes: Filter by NACE 2008 activity codes (e.g. ["62010"]).
        juridical_form_codes: Filter by juridical form codes (e.g. ["015"]).
        zip_codes: Filter by exact zip codes (e.g. ["1040", "1050"]).
        legal_person_types: Filter by legal person type codes.
        start_date_from: Range filter start date from (YYYYMMDD).
        start_date_to: Range filter start date to (YYYYMMDD).
        zip_code_from: Range filter zip code from.
        zip_code_to: Range filter zip code to.
    """
    body: dict = {"q": q, "page": str(page), "max": str(max_results)}

    if active is not None:
        body["active"] = str(active).lower()
    if has_phone is not None:
        body["has_phone"] = str(has_phone).lower()
    if has_email is not None:
        body["has_email"] = str(has_email).lower()
    if has_website is not None:
        body["has_website"] = str(has_website).lower()

    terms_filters: dict = {}
    if activity_codes:
        terms_filters["activity"] = activity_codes
    if juridical_form_codes:
        terms_filters["juridical_form"] = juridical_form_codes
    if zip_codes:
        terms_filters["zip_code"] = zip_codes
    if legal_person_types:
        terms_filters["legal_person_type"] = legal_person_types
    if terms_filters:
        body["terms_filters"] = terms_filters

    range_filters: dict = {}
    if start_date_from or start_date_to:
        range_filters["start_date"] = {}
        if start_date_from:
            range_filters["start_date"]["from"] = start_date_from
        if start_date_to:
            range_filters["start_date"]["to"] = start_date_to
    if zip_code_from or zip_code_to:
        range_filters["zip_code"] = {}
        if zip_code_from:
            range_filters["zip_code"]["from"] = zip_code_from
        if zip_code_to:
            range_filters["zip_code"]["to"] = zip_code_to
    if range_filters:
        body["range_filters"] = range_filters

    data = await _post("/companies/search", body)
    return json.dumps(data, indent=2, ensure_ascii=False)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
