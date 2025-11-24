function [area, perimetro, desviacion_color, asimetria] = procesar(ruta_imagen)
    % IMPORTANTE: Esta palabra 'function' debe ser lo PRIMERO en el archivo.
    
    % Evitar error grafico
    try
        graphics_toolkit("gnuplot");
    catch
    end
    warning('off', 'all');
    pkg load image;

    % Forzar ruta a texto
    ruta_imagen = char(ruta_imagen);

    try
        im = imread(ruta_imagen);
    catch
        area = 0; perimetro = 0; desviacion_color = 0; asimetria = 0;
        return;
    end

    im = imresize(im, [256, 256]);
    if size(im, 3) == 3
        img_gray = rgb2gray(im);
    else
        img_gray = im;
    end

    try
        nivel = graythresh(img_gray);
        mapa = im2bw(img_gray, nivel);
    catch
        mapa = img_gray < 128;
    end

    if mean(mapa(:)) > 0.5
       mapa = ~mapa;
    end
    
    mapa = bwareaopen(mapa, 50);
    mapa = imfill(mapa, 'holes');

    area = sum(mapa(:));
    
    perim_img = bwperim(mapa);
    perimetro = sum(perim_img(:));
    
    pix = img_gray(mapa);
    if isempty(pix)
        desviacion_color = 0;
    else
        desviacion_color = std(double(pix));
    end

    [r, c] = size(mapa);
    mid = floor(c/2);
    izq = mapa(:, 1:mid);
    der = mapa(:, end-mid+1:end);
    der_flip = fliplr(der);
    
    if size(izq, 2) != size(der_flip, 2)
        m = min(size(izq, 2), size(der_flip, 2));
        izq = izq(:, 1:m);
        der_flip = der_flip(:, 1:m);
    end

    asimetria = sum(sum(xor(izq, der_flip))) / (area + 1);
endfunction