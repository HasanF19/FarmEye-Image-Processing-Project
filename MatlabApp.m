folder_path = 'Dosya isminiz'; 
image_files = dir(fullfile(folder_path, '*.png'));

file_dates = struct('name', {}, 'date', []);

for i = 1:length(image_files)
    file_name = image_files(i).name;
   
    tokens = regexp(file_name, '\d{4}-\d{2}-\d{2}', 'match');
    if ~isempty(tokens)
        file_dates(end+1).name = file_name;
        file_dates(end).date = datetime(tokens{1}, 'InputFormat', 'yyyy-MM-dd');
    end
end

[~, sorted_idx] = sort([file_dates.date]);
file_dates = file_dates(sorted_idx);

% "Pembe" renk aralığını tanımlayın
lower_pink = [200, 0, 200]; % Pembe için alt sınır (RGB)
upper_pink = [255, 100, 255]; % Pembe için üst sınır (RGB)

% Yangın oranlarını hesaplamak için değişken
dates = [file_dates.date];
fire_ratios = zeros(1, length(file_dates));

% Her bir görüntü üzerinde işlem yap
for i = 1:length(file_dates)
    % Görüntü dosyasının tam yolunu alın
    image_path = fullfile(folder_path, file_dates(i).name);
    
    % Görüntüyü yükle
    image = imread(image_path);
    
    % Binary maske oluştur (yanmış alanlar için)
    pink_mask = (image(:,:,1) >= lower_pink(1) & image(:,:,1) <= upper_pink(1)) & ...
                (image(:,:,2) >= lower_pink(2) & image(:,:,2) <= upper_pink(2)) & ...
                (image(:,:,3) >= lower_pink(3) & image(:,:,3) <= upper_pink(3));
    
    % Toplam piksel sayısını ve yanmış alan oranını hesapla
    total_pixels = numel(pink_mask);
    burned_pixels = sum(pink_mask(:));
    fire_ratios(i) = (burned_pixels / total_pixels) * 100; % Yüzde olarak
    
    binary_image = uint8(pink_mask) * 255;
    binary_image_name = fullfile(folder_path, ['binary_' file_dates(i).name]);
    imwrite(binary_image, binary_image_name);
end


fprintf('Tarih ve yangın oranları:\n');
for i = 1:length(file_dates)
    fprintf('%s - Yangın Oranı: %.2f%%\n', datestr(file_dates(i).date), fire_ratios(i));
end

r
figure;
plot(dates, fire_ratios, '-o');
xlabel('Tarih');
ylabel('Yangın Oranı (%)');
title('Tarih Bazında Yangın Oranları');
grid on;

% Yangın oranı %0'dan büyük olan günler için bir tablo oluştur
fire_days = file_dates(fire_ratios > 0);
fire_ratios_filtered = fire_ratios(fire_ratios > 0); 

% Tarih ve yangın oranlarını bir tabloya ekle
fire_table = table({fire_days.name}', [fire_days.date]', fire_ratios_filtered', ...
                   'VariableNames', {'DosyaAdı', 'Tarih', '%yangın oramı'});

% Excel dosyasına yaz
excel_file_name = fullfile(folder_path, 'YangınlıGünler.xlsx');
writetable(fire_table, excel_file_name);

fprintf('Yangın olan günlerin sonuçları "%s" dosyasına yazdırıldı.\n', excel_file_name);
