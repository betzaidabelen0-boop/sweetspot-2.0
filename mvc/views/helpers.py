def formato_precio(precio) -> str:
    """Devuelve el precio como $15 o $15.50 (sin decimales si es entero)."""
    try:
        valor = float(precio)
    except (TypeError, ValueError):
        return ""
    if valor == int(valor):
        return f"${int(valor):,}"
    return f"${valor:,.2f}"
