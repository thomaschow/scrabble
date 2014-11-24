function [] = run()

    images = dir('*.png'), dir('*.PNG')
    
    for i = 1:length(images)
        figure(i);
        extract_board(images(i).name);
    end
end