function [area, perimetro, desviacion_color, asimetria] = segmentar_lunar(ruta_imagen)
    % IMPORTANTE: La palabra 'function' debe estar en la linea 1
    
    % Configuración de seguridad para evitar errores gráficos
    try
        graphics_toolkit("gnuplot");
    catch
        % Nada
    end
    warning('off', 'all');

    pkg load image;

    % Asegurar que la ruta es texto
    ruta_imagen = char(ruta_imagen);

    % 1. Leer imagen
    try
        im_original = imread(ruta_imagen);
    catch
        % Si falla, devolvemos ceros
        area = 0; perimetro = 0; desviacion_color = 0; asimetria = 0;
        return;
    end

    % 2. Preprocesamiento
    im = imresize(im_original, [256, 256]);
    if size(im, 3) == 3
        img_gray = rgb2gray(im);
    else
        img_gray = im;
    end

    % 3. Segmentación
    try
        nivel = graythresh(img_gray);
        mapa_binario = im2bw(img_gray, nivel);
    catch
        mapa_binario = img_gray < 128;
    end

    % Invertir si es necesario
    if mean(mapa_binario(:)) > 0.5
       mapa_binario = ~mapa_binario;
    end
    
    mapa_binario = bwareaopen(mapa_binario, 50);
    mapa_binario = imfill(mapa_binario, 'holes');

    % 4. Extraer datos
    area = sum(mapa_binario(:));
    
    perim_img = bwperim(mapa_binario);
    perimetro = sum(perim_img(:));
    
    pixeles_lunar = img_gray(mapa_binario);
    if isempty(pixeles_lunar)
        desviacion_color = 0;
    else
        desviacion_color = std(double(pixeles_lunar));
    end

    [rows, cols] = size(mapa_binario);
    centro_col = floor(cols/2);
    izq = mapa_binario(:, 1:centro_col);
    der = mapa_binario(:, end-centro_col+1:end);
    der_flip = fliplr(der);
    
    % Ajuste de dimensiones impares
    if size(izq, 2) != size(der_flip, 2)
        min_col = min(size(izq, 2), size(der_flip, 2));
        izq = izq(:, 1:min_col);
        der_flip = der_flip(:, 1:min_col);
    end

    asimetria = sum(sum(xor(izq, der_flip))) / (area + 1);
end