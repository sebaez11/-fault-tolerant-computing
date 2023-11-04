import fetch from 'node-fetch';
import cheerio from 'cheerio';
import pc from "picocolors";
import { exec } from "child_process";

const song = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

const urls = [
  'https://www.clevercel.co/products/samsung-galaxy-note-20',
  'https://www.clevercel.co/products/samsung-galaxy-s20-plus',
  'https://www.clevercel.co/products/samsung-galaxy-s21-5g',
  'https://saldos.clevercel.co/products/samsung-galaxy-s21-5g',
];

function checkAvailability() {
  console.clear();
  for (let i = 0; i < urls.length; i++) {
    fetch(urls[i])
      .then(response => response.text())
      .then(data => {
        const $ = cheerio.load(data);
        const productMetaTitle = $('.product-meta__title').text();
        const productMetaLabel = $('.product-meta__label-list');
        const productSalePrice = $('.product-meta__price-list-container').find('.price--highlight').text().split('$')[1];

        if (productMetaLabel.length > 0 && !productMetaLabel.find('span:contains("Agotado")').length) {
          console.log(productMetaTitle.padEnd(30), pc.green('Disponible').padEnd(25), pc.blue(`$${productSalePrice}`).padEnd(10), pc.yellow(urls[i]));
          
          if (productMetaTitle === 'Samsung Galaxy S20 Plus' || productMetaTitle === 'Samsung Galaxy Note 20') {
            exec(`start ${song}`);
          }

        } else {
          console.log(productMetaTitle.padEnd(30), pc.red('Agotado').padEnd(25), pc.gray(`$${productSalePrice}`).padEnd(10), pc.gray(urls[i]));
        }
      })
      .catch(error => {
        console.log(pc.red('Error al realizar la solicitud:', error.message));
      });
  }
}

setInterval(checkAvailability, 40000);

checkAvailability();
