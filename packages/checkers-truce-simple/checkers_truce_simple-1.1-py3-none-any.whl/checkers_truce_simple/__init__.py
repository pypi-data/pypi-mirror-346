import os as _os, sys as _sys, json as _json

__stdout = _sys.stdout
with open(_os.devnull, 'w') as _sys.stdout:
    import pygame as _pygame
_sys.stdout = __stdout
 
# chess battle advanced
# chess battle advanced
# chess battle advanced
# chess battle advanced
# chess battle advanced
# chess battle advanced
# chess battle advanced
# chess battle advanced

def cts():
    _os.chdir(_os.path.dirname(__file__))

    _pygame.init()
    _pygame.mixer.init()

    screen = _pygame.display.set_mode((1280, 720))
    _pygame.display.set_caption('checkers truce simple')
    _pygame.display.set_icon(_pygame.image.load('wylcomebyck.png'))

    _pygame.mixer.music.load('cts.mp3')
    _pygame.mixer.music.play(-1)
    win_sound = _pygame.mixer.Sound('victory.wav')

    font_big = _pygame.font.Font('georgia.ttf', 80)
    font_small = _pygame.font.Font('georgia.ttf', 50)
    font_medium = _pygame.font.Font('georgia.ttf', 60)

    cts_image = _pygame.image.load('cts.png')
    walcome_image = _pygame.image.load('walcome.png')

    reset_text = font_big.render('The army has been reset.', 0, (0, 0, 0))
    back_text = font_small.render('Back', 0, (0, 0, 0))
    remove_piece_text  = font_medium.render('Choose a piece to remove:', 0, (0, 0, 0))
    checker_deletion_text = font_big.render('"checker" has been deleted.', 0, (0, 0, 0))
    settings_text = font_medium.render('no settings', 0, (0, 0, 0))

    clock = _pygame.time.Clock()

    consent = True


    def reset_army():
        with open('stuff.json') as f:
            json_dict = _json.load(f)
        json_dict['army'] = ['checker', 'checker', 'checker', 'checker', 'checker', 'checker', 'checker', 'checker', 'checker', 'checker', 'checker', 'checker']
        with open('stuff.json', 'w') as f:
            _json.dump(json_dict, f, indent=2)
            
        screen.fill((255, 255, 255))
        text_rect = reset_text.get_rect()
        text_rect.center = (640, 360)
        screen.blit(reset_text, text_rect)
        screen.blit(back_text, (5, 5))
        
        while True:
            for event in _pygame.event.get():
                if event.type == _pygame.QUIT:
                    _pygame.quit()
                    _sys.exit()
                    
                elif event.type == _pygame.MOUSEBUTTONDOWN:
                    if event.pos[1] <= 70:
                        return
                        
            _pygame.display.flip()
            clock.tick(30)
        
    def remove_piece():
        with open('stuff.json') as f:
            json_dict = _json.load(f)
            
        screen.fill((255, 255, 255))
        text_rect = remove_piece_text.get_rect()
        text_rect.center = (640, 125)
        screen.blit(remove_piece_text, text_rect)
        screen.blit(back_text, (5, 5))
        
        if json_dict['army']:
            checker_text = font_small.render('checker', 0, (0, 0, 0))
            checker_text_rect = checker_text.get_rect()
            checker_text_rect.center = (640, 470)
            _pygame.draw.rect(screen, (204, 203, 202), (530, 240, 220, 280))
            _pygame.draw.rect(screen, (156, 155, 154), (530, 240, 220, 280), 6)
            _pygame.draw.circle(screen, (252, 11, 10), (640, 345), 90)
            _pygame.draw.circle(screen, (12, 11, 10), (640, 345), 90, 8)
            screen.blit(checker_text, checker_text_rect)
        else:
            no_piece_text = font_small.render('no pieces', 0, (0, 0, 0))
            no_piece_text_rect = no_piece_text.get_rect()
            no_piece_text_rect.center = (640, 300)
            screen.blit(no_piece_text, no_piece_text_rect)
        
        clicked_checker = False
        while True:
            for event in _pygame.event.get():
                if event.type == _pygame.QUIT:
                    _pygame.quit()
                    _sys.exit()
                    
                elif event.type == _pygame.MOUSEBUTTONDOWN:
                    if event.pos[1] <= 70:
                        return
                    elif event.pos[0] >= 527 and event.pos[1] >= 237 and event.pos[0] <= 753 and event.pos[1] <= 523 and json_dict['army']:
                        clicked_checker = True
            
            if clicked_checker:
                break
            
            _pygame.display.flip()
            clock.tick(30)
        
        json_dict['army'] = []
        with open('stuff.json', 'w') as f:
            _json.dump(json_dict, f, indent=2)
        
        screen.fill((255, 255, 255))
        text_rect = checker_deletion_text.get_rect()
        text_rect.center = (640, 360)
        screen.blit(checker_deletion_text, text_rect)
        screen.blit(back_text, (5, 5))
        
        while True:
            for event in _pygame.event.get():
                if event.type == _pygame.QUIT:
                    _pygame.quit()
                    _sys.exit()
                    
                elif event.type == _pygame.MOUSEBUTTONDOWN:
                    if event.pos[1] <= 70:
                        return
                        
            _pygame.display.flip()
            clock.tick(30)
        
    def settings():
        screen.fill((255, 255, 255))
        text_rect = settings_text.get_rect()
        text_rect.center = (640, 125)
        screen.blit(settings_text, text_rect)
        screen.blit(back_text, (5, 5))
        screen.blit(walcome_image, (0, 240))
        
        while True:
            for event in _pygame.event.get():
                if event.type == _pygame.QUIT:
                    _pygame.quit()
                    _sys.exit()
                    
                elif event.type == _pygame.MOUSEBUTTONDOWN:
                    if event.pos[1] <= 70:
                        return
                        
            _pygame.display.flip()
            clock.tick(30)
        
    def play():
        with open('stuff.json') as f:
            json_dict = _json.load(f)
            
        screen.fill((255, 255, 255))
        screen.blit(back_text, (5, 5))
        _pygame.draw.rect(screen, (156, 155, 154), (375, 175, 530, 530), 10)
        _pygame.draw.rect(screen, (236, 235, 234), (380, 180, 520, 520))
        for y in range(8):
            for x in range(8):
                if (x+y)%2 == 0:
                    _pygame.draw.rect(screen, (12, 11, 10), (380 + x*65, 180 + y*65, 65, 65))
                    if y > 4 and json_dict['army']:
                        _pygame.draw.circle(screen, (252, 11, 10), (412 + x*65, 212 + y*65), 25)
        text1 = font_small.render('there is no battle' if json_dict['army'] else 'you have no army', 0, (0, 0, 0))
        text2 = font_small.render('you win' if json_dict['army'] else 'you lose', 0, (0, 0, 0))
        text1_rect = text1.get_rect()
        text2_rect = text2.get_rect()
        text1_rect.center = (640, 40)
        text2_rect.center = (640, 100)
        screen.blit(text1, text1_rect)
        screen.blit(text2, text2_rect)
                    
        while True:
            for event in _pygame.event.get():
                if event.type == _pygame.QUIT:
                    _pygame.quit()
                    _sys.exit()
                    
                elif event.type == _pygame.MOUSEBUTTONDOWN:
                    if json_dict['army']:
                        win_sound.play()
                    if event.pos[1] <= 70 and event.pos[0] < 200:
                        return
                        
            _pygame.display.flip()
            clock.tick(30)
            

    while True:
        for event in _pygame.event.get():
            if event.type == _pygame.QUIT:
                _pygame.quit()
                _sys.exit()
                
            elif event.type == _pygame.MOUSEBUTTONDOWN:
                if event.pos[1] >= 155 and event.pos[1] < 235:
                    _pygame.quit()
                    _sys.exit()
                elif event.pos[1] >= 235 and event.pos[1] < 310:
                    reset_army()
                elif event.pos[1] >= 310 and event.pos[1] < 380:
                    remove_piece()
                elif event.pos[1] >= 380 and event.pos[1] < 450:
                    settings()
                elif event.pos[1] >= 450 and event.pos[1] < 525:
                    play()
                    
        screen.blit(cts_image, (0, 0))
                    
        _pygame.display.flip()
        clock.tick(30)
        
if __name__ == '__main__':
    cts()