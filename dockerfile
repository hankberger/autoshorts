FROM python:3.9

WORKDIR /app

COPY . .

RUN apt-get update \
    && apt-get install -qq -y build-essential xvfb xdg-utils wget ffmpeg libpq-dev vim libmagick++-dev fonts-liberation sox bc --no-install-recommends\
    && apt-get clean

COPY requirements.txt .

RUN pip install -r requirements.txt

## ImageMagicK Installation ##
# RUN mkdir -p /tmp/distr && \
#     cd /tmp/distr && \
#     wget https://download.imagemagick.org/ImageMagick/download/releases/ImageMagick-7.0.11-2.tar.xz && \
#     tar xvf ImageMagick-7.0.11-2.tar.xz && \
#     cd ImageMagick-7.0.11-2 && \
#     ./configure --enable-shared=yes --disable-static --without-perl && \
#     make && \
#     make install && \
#     ldconfig /usr/local/lib && \
#     cd /tmp && \
#     rm -rf distr

## Installing External Fonts ##
# RUN mkdir -p /usr/share/fonts/truetype/custom \
#     && for fontname in \
#     'Mrs Saint Delafield' 'Arimo' 'Dosis'; \
#     do \
#     modified_fontname=$fontname//[ ]/_}; \
#     wget "https://fonts.google.com/download?family=$fontname" -O $modified_fontname.zip; \
#     mkdir -p /usr/share/fonts/truetype/custom; \
#     unzip $modified_fontname.zip -d /usr/share/fonts/truetype/custom; \
#     rm $modified_fontname.zip; \
#     done



CMD [ "python", "-u", "main.py"]