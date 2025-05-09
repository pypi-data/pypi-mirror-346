import registry_service.cli as cli_module
import registry_service.service as service_module


def test_cli_main_invokes_uvicorn_run(monkeypatch):
    called = {}

    def fake_run(app, host, port):
        # Capture parameters
        called['app'] = app
        called['host'] = host
        called['port'] = port

    # Monkeypatch uvicorn.run in the CLI module
    monkeypatch.setattr(cli_module.uvicorn, 'run', fake_run)

    # Invoke main()
    cli_module.main()

    # Ensure uvicorn.run was called with correct arguments
    assert 'app' in called and called['app'] is service_module.app
    assert called.get('host') == '0.0.0.0'
    assert called.get('port') == 8000