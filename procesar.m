function [area, perimetro, desviacion_color, asimetria] = procesar(ruta_imagen, debug_mode)
    % Si no mandan el segundo argumento, asumimos falso
    if nargin < 2
        debug_mode = 0;
    end

    % Configuración anti-error
    try
        graphics_toolkit("gnuplot");
    catch
    end
    warning('off', 'all');
    pkg load image;

    ruta_imagen = char(ruta_imagen);

    try
        im = imread(ruta_imagen);
    catch
        area=0; perimetro=0; desviacion_color=0; asimetria=0; return;
    end

    im = imresize(im, [256, 256]);
    if size(im, 3) == 3
        img_gray = rgb2gray(im);
    else
        img_gray = im;
    end

    % --- SEGMENTACIÓN MEJORADA (OTSU) ---
    try
        nivel = graythresh(img_gray);
        mapa = im2bw(img_gray, nivel);
    catch
        mapa = img_gray < 128;
    end

    % Lógica: Si las esquinas son blancas, invertir (porque el lunar debe ser blanco)
    if mapa(1,1) == 1 && mapa(1, end) == 1
       mapa = ~mapa;
    end
    
    % Limpieza agresiva de ruido
    mapa = bwareaopen(mapa, 100); % Borra manchas menores a 100px
    mapa = imfill(mapa, 'holes'); % Rellena agujeros dentro del lunar

    % --- GUARDAR IMAGEN DE PRUEBA (SOLO SI SE PIDE) ---
    if debug_mode == 1
        % Pone un borde verde alrededor de lo detectado sobre la original
        borde = bwperim(mapa);
        im_debug = im;
        R = im_debug(:,:,1); G = im_debug(:,:,2); B = im_debug(:,:,3);
        R(borde) = 0; G(borde) = 255; B(borde) = 0; % Linea Verde
        im_debug = cat(3, R, G, B);
        imwrite(im_debug, 'octave_debug_view.jpg');
    end
    
    % --- CÁLCULOS ---
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
end