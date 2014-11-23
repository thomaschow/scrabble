function [out] = scrabble_prototype(in)
    img = imread(in);
    img = imresize(img, [528 320]);
    img = rgb2gray(img);
    level = multithresh(img, 15);
    
    thresholded_img = imquantize(img, level);
    
    
    %Letters that were just played
    %imshow(thresholded_img, [15,16]);
    new_letters = thresholded_img == 15 | thresholded_img == 16;
    
    cc_new_letters = bwconncomp(new_letters);
    reg_new_letters = regionprops(new_letters, 'Area' );
    new_letters = xor(bwareaopen(new_letters,30),  bwareaopen(new_letters,100));

    %imshow(new_letters)
    
    %Letters that were already on the board
    
    %imshow(thresholded_img, [1,4]);
    
    old_letters = thresholded_img < 4;
    
    all_letters = new_letters | old_letters;
    
    imshow(all_letters);

    %imshow(old_letters);
    
    %Boundary that defines the board
    %imshow(thresholded_img, [10,11]);
    
    boundary = thresholded_img >= 12 & thresholded_img <= 15;
    
    %imshow(boundary);
    
    big_chunks = regionprops(boundary, 'Area', 'PixelIdxList', 'MinorAxisLength');
    
    i = find([big_chunks.Area] == max([big_chunks.Area]));
    
    big_chunks(i).MinorAxisLength;
    
    boundary(:) = 0;
    boundary(big_chunks(i).PixelIdxList) = 1;
    bottom_chunk = regionprops(imcomplement(boundary), 'Area', 'PixelIdxList', 'MinorAxisLength');
    
    i = find([bottom_chunk.Area] == max([bottom_chunk.Area]));
    boundary(:) = 0;
    boundary(bottom_chunk(i).PixelIdxList) = 1;
    
    coords = ind2sub( size(boundary), bottom_chunk(i).PixelIdxList);
    [r,c] = ind2sub(size(boundary), min(coords(:, 1)));
    boundary(:) = 1;
    boundary(1:r - 280, :) = 0;
    boundary(r:end, :) = 0;
    board = all_letters & boundary;
    out = board;
    
end