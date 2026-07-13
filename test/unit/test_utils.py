"""Unit tests for webhook signature verification helpers."""

from notion_py_client.utils import sign_webhook_payload, verify_webhook_signature


class TestWebhookSignature:
    """Test sign_webhook_payload / verify_webhook_signature."""

    def test_sign_webhook_payload_matches_manual_hmac(self):
        signature = sign_webhook_payload(
            body='{"verification_token":"secret-token"}',
            verification_token="my-verification-token",
        )

        assert signature.startswith("sha256=")
        assert len(signature) == len("sha256=") + 64

    def test_verify_webhook_signature_accepts_matching_signature(self):
        body = '{"type":"page.created"}'
        token = "my-verification-token"
        signature = sign_webhook_payload(body=body, verification_token=token)

        assert verify_webhook_signature(
            body=body, signature=signature, verification_token=token
        )

    def test_verify_webhook_signature_rejects_tampered_body(self):
        token = "my-verification-token"
        signature = sign_webhook_payload(
            body='{"type":"page.created"}', verification_token=token
        )

        assert not verify_webhook_signature(
            body='{"type":"page.deleted"}',
            signature=signature,
            verification_token=token,
        )

    def test_verify_webhook_signature_rejects_wrong_token(self):
        body = '{"type":"page.created"}'
        signature = sign_webhook_payload(body=body, verification_token="token-a")

        assert not verify_webhook_signature(
            body=body, signature=signature, verification_token="token-b"
        )

    def test_verify_webhook_signature_rejects_missing_signature(self):
        assert not verify_webhook_signature(
            body="{}", signature=None, verification_token="token"
        )

    def test_verify_webhook_signature_accepts_bytes_body(self):
        token = "my-verification-token"
        body = b'{"type":"page.created"}'
        signature = sign_webhook_payload(body=body, verification_token=token)

        assert verify_webhook_signature(
            body=body, signature=signature, verification_token=token
        )
