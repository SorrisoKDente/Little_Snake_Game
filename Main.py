from code.Menu import Menu

if __name__ == "__main__":
    while True:
        try:
            menu = Menu()
            menu.run()
        except SystemExit:
            # Se o jogo foi fechado corretamente
            break
        except Exception as e:
            # Se houve algum erro, mostra e tenta reiniciar
            print(f"Erro no jogo: {e}")
            import traceback
            traceback.print_exc()
            print("Reiniciando o menu...")