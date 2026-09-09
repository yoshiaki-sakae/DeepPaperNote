from __future__ import annotations

import ssl
from pathlib import Path

import common
import pytest

FIXTURE_CA = Path(__file__).parent / "fixtures" / "test_root_ca.pem"
FIXTURE_CA_CN = "DeepPaperNote Test Root CA"


def _trusted_common_names(context: ssl.SSLContext) -> set[str]:
    names: set[str] = set()
    for cert in context.get_ca_certs():
        for rdn in cert.get("subject", ()):
            for key, value in rdn:
                if key == "commonName":
                    names.add(value)
    return names


def test_https_ssl_context_trusts_ca_from_ssl_cert_file(monkeypatch: pytest.MonkeyPatch) -> None:
    # 社内 Proxy(SSL インスペクション)の Root CA を SSL_CERT_FILE で追加できること
    monkeypatch.setenv("SSL_CERT_FILE", str(FIXTURE_CA))

    context = common.https_ssl_context("https://arxiv.org/pdf/1706.03762.pdf")

    assert context is not None
    assert FIXTURE_CA_CN in _trusted_common_names(context)


def test_https_ssl_context_keeps_certifi_bundle(monkeypatch: pytest.MonkeyPatch) -> None:
    # 追加 CA を指定しても certifi の公開 CA は引き続き信頼されること
    pytest.importorskip("certifi")
    monkeypatch.setenv("SSL_CERT_FILE", str(FIXTURE_CA))

    context = common.https_ssl_context("https://arxiv.org/pdf/1706.03762.pdf")

    assert context is not None
    names = _trusted_common_names(context)
    assert FIXTURE_CA_CN in names
    assert "ISRG Root X1" in names


def test_https_ssl_context_returns_none_for_plain_http() -> None:
    assert common.https_ssl_context("http://example.org/paper.pdf") is None
