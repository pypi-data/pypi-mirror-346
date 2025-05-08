# https://cryptography.io/en/latest/x509/ocsp/
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.x509 import load_pem_x509_certificate, ocsp

def query_ocsp(cert, issuer):
    cert = load_pem_x509_certificate(pem_cert)
    issuer = load_pem_x509_certificate(pem_issuer)
    builder = ocsp.OCSPRequestBuilder()

    # SHA256 is in this example because while RFC 5019 originally
    # required SHA1 RFC 6960 updates that to SHA256.
    # However, depending on your requirements you may need to use SHA1
    # for compatibility reasons.
    builder = builder.add_certificate(cert, issuer, SHA256())
    req = builder.build()
    base64.b64encode(req.public_bytes(serialization.Encoding.DER))
    b'MF8wXTBbMFkwVzANBglghkgBZQMEAgEFAAQgn3BowBaoh77h17ULfkX6781dUDPD82Taj8wO1jZWhZoEINxPgjoQth3w7q4AouKKerMxIMIuUG4EuWU2pZfwih52AgI/IA=='

    # send request

    ocsp_resp = ocsp.load_der_ocsp_response(der_ocsp_resp_unauth)
    print(ocsp_resp.response_status)
    # OCSPResponseStatus.UNAUTHORIZED
    return ocsp_resp.response_status
