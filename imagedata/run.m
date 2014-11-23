function [] = run()

    images = {'IMG_1510.png'; 
              'IMG_1511.png'; 
              '2014-11-23 01.41.33.png'; 
              '2014-11-23 01.41.40.png'; 
              '2014-11-23 01.41.45.png'};

    for i = 1:5
        figure(i);
        imshow(scrabble_prototype(images{i}));
    end
end