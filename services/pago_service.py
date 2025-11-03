from models.pago import Pago
from models.boleta import Boleta
from repositories.pago_repo import PagoRepository
from repositories.boleta_repo import BoletaRepository

pago_repo = PagoRepository()
boleta_repo = BoletaRepository()

async def procesar_pago(pago: Pago):
    # Registrar pago
    idPago = await pago_repo.crear(pago.dict())

    # Confirmar pago
    await pago_repo.confirmar(idPago)

    # Generar boleta
    boleta = Boleta(idUsuario=pago.idUsuario, total=pago.monto)
    idBoleta = await boleta_repo.crear(boleta.dict())

    return {
        "estado": "pago confirmado",
        "idPago": idPago,
        "idBoleta": idBoleta
    }
