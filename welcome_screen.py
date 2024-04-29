import pygame
import pygame_gui

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Slot Machine")

white = (255, 255, 255)
light_blue = (173, 216, 230) 
light_gray = (220, 220, 220)   
black = (0, 0, 0)

manager = pygame_gui.UIManager((width, height))


font_title = pygame.font.Font(None, 48) 

title_text = pygame_gui.elements.UITextBox(
    relative_rect=pygame.Rect((95, 40), (610, 100)),  
    html_text='<div style="text-align: center;"><span style="font-size: 55px; color: black; font-weight: bold;">Dobrodosli u Slot Machine<br>Nakon sto unesete balans racuna i ulog po liniji, bicete preusmereni na igru.<br>Kad se igra ucita, pritiskom na Space zabava pocinje!</span></div>',
    manager=manager,
)

input_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((200, 150), (400, 40)),
    text='Unesite iznos i ulog po liniji:',
    manager=manager,
    object_id='#input_label'
)

input_box1 = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((200, 200), (400, 40)),
    manager=manager
)
input_box2 = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((200, 260), (400, 40)),
    manager=manager
)
submit_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((350, 320), (100, 40)),
    text='Potvrdi',
    manager=manager
)

result_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((200, 380), (400, 40)),
    text='',
    manager=manager
)

clock = pygame.time.Clock()
running = True
submit_clicked = False

while running:          #game loop welcome screen-a
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Procesiranje UI događaja
        manager.process_events(event)

        # Provera da li je pritisnuto dugme "Potvrdi"
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == submit_button:
                    try:
                        number1 = float(input_box1.get_text())
                        number2 = float(input_box2.get_text())
                        
                        if number2 <= number1:
                            result_label.set_text(f"Uneli ste iznos od {number1}$ i ulog {number2}$. Preusmeravanje.")
                            submit_clicked = True  # Postavi flag da je dugme kliknuto
                        else:
                            result_label.set_text("Ulog ne moze biti veci od ukupnog iznosa.")
                    
                    except ValueError:
                        result_label.set_text("Unesite validne brojeve.")

    screen.fill(black)
 
    #crtanje 
    pygame.draw.rect(screen, light_blue, (180, 190, 440, 180))  
    pygame.draw.rect(screen, black, (180, 190, 440, 180), 2)     

    manager.update(time_delta)
    manager.draw_ui(screen)

    pygame.display.flip()

    # Provera da li je kliknuto dugme i zatvori prozor ako jeste
    if submit_clicked:
        pygame.time.wait(3000)  # sacekaj neko vrijeme
        running = False  

pygame.quit()
