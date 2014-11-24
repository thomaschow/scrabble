function [out] = extract_board(in)
    img = imread(in);
    img = imresize(img, [528 320]);
    img = rgb2gray(img);
    level = multithresh(img, 15);
    
    thresholded_img = imquantize(img, level);
    
    %Letters that were just played
    %imshow(thresholded_img, [15,16]);
    new_letters = thresholded_img >= 16 & thresholded_img <= 17;
    
    cc_new_letters = bwconncomp(new_letters);
    reg_new_letters = regionprops(new_letters, 'Area' );
    new_letters = xor(bwareaopen(new_letters,20),  bwareaopen(new_letters,100));

    %imshow(new_letters)
    %Letters that were already on the board
    
    %imshow(thresholded_img, [1,4]);
    
    old_letters = thresholded_img <5;
    
    
    old_letters = xor(bwareaopen(old_letters, 20), bwareaopen(old_letters, 100));
    
    
    all_letters = new_letters | old_letters;
    
    %imshow(all_letters);

    %imshow(old_letters);
    
    %Boundary that defines the board
    %imshow(thresholded_img, [10,11]);
    
    boundary = thresholded_img >= 12 & thresholded_img <= 15;
    
    %imshow(boundary);
    
    big_chunks = regionprops(boundary, 'Area', 'PixelIdxList', 'MinorAxisLength');
    
    i = find([big_chunks.Area] == max([big_chunks.Area]));
    
    boundary(:) = 0;
    boundary(big_chunks(i).PixelIdxList) = 1;
    bottom_chunk = regionprops(imcomplement(boundary), 'Area', 'PixelIdxList', 'MinorAxisLength');
    
    i = find([bottom_chunk.Area] == max([bottom_chunk.Area]));
    boundary(:) = 0;
    boundary(bottom_chunk(i).PixelIdxList) = 1;
    
    coords = ind2sub( size(boundary), bottom_chunk(i).PixelIdxList);
    [r,c] = min(coords(:, 1));
    boundary(:) = 1;
    boundary(1:r - 320, :) = 0;
    boundary(r:end, :) = 0;
    
    %imshow (boundary);
    board = all_letters & boundary;
    
    figure, imshow(board);  
    
    board = bwlabel(board, 8);
    n=max(board(:));
    letters = regionprops(board, 'BoundingBox');
    letts=cell(n,1);
    
    offs = 0;
    for i = 1:n
        box = ceil(letters(i).BoundingBox);
        offs = ceil(max([offs, box(3), box(4)]));
    end
    for i = 1:n
        box = ceil(letters(i).BoundingBox);
        idx_x=[box(1)-5 box(1)+15];
        idx_y=[box(2)-5 box(2)+15];
        if idx_x(1)<1, idx_x(1)=1; end
        if idx_y(1)<1, idx_y(1)=1; end
        if idx_x(2)>size(board, 2), idx_x(2)=size(board, 2); end
        if idx_y(2)>size(board, 1), idx_y(2)=size(board, 1); end
        im=board==i;
        letts{i}=imresize(im(idx_y(1):idx_y(2),idx_x(1):idx_x(2)), [30,30]);
    end
    
    for i = 1:n
        %subplot(5, ceil(n/5.0), i);
        %imshow(letts{i});
        imwrite(letts{i}, ['letter_data/',in, '_letter_',int2str(i),'.png'] );
    end
    out = board;
end