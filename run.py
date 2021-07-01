from medic import create_app

if __name__ == '__main__':

    medic_app = create_app()

    medic_app.run(debug=True, host='127.0.0.1', port='5000')
    
