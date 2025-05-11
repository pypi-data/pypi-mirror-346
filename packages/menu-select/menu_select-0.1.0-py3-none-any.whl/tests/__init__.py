"""Test suite for menu_select package."""
import pytest
from menu_select import Menu_select as ms


class TestMenuSelect:
    """Test cases for the Menu_select class."""

    def setup_method(self):
        """Set up a Menu_select instance for testing."""
        self.menu = ms(cabeçalho='cabeçalho', texto_seleção=['negrito', 'vermelho', 'azul'])

    def test_options(self, monkeypatch):
        """Test the options method."""
        opt = ['Logar', 'sair']
        # Simula a entrada do usuário para selecionar a primeira opção (índice 0)
        monkeypatch.setattr('builtins.input', lambda _: '0')
        escolha = self.menu.options(descrição='Essa é a descrição', opções=opt, limite_opçoes=3)
        assert escolha in range(len(opt)), "Escolha deve estar dentro do intervalo de opções."