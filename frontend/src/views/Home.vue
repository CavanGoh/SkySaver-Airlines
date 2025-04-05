<template>
  <div class="home-container">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="main-title">Explore the World with SkySaver Airlines</h1>
        <p class="subtitle">Fly to your dream destinations with comfort and style</p>
        <router-link to="book" class="cta-button">Book Now</router-link>
      </div>
    </section>

    <!-- Featured Destinations -->
    <section class="featured-destinations">
      <h2 class="section-title">Popular Destinations</h2>
      <div class="destinations-grid">
        <div class="destination-card" v-for="(destination, index) in destinations" :key="index">
          <div class="destination-image" :style="{ backgroundImage: `url(${destination.imageUrl})` }">
            <div class="destination-overlay">
              <h3>{{ destination.name }}</h3>
              <p>{{ destination.subtitle }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Why Choose Us -->
    <section class="features-section">
      <h2 class="section-title">Why Choose SkySaver</h2>
      <div class="features-grid">
        <div class="feature-card" v-for="(feature, index) in features" :key="index">
          <div class="feature-icon" v-html="feature.icon"></div>
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.description }}</p>
        </div>
      </div>
    </section>

    <!-- Testimonials -->
    <section class="testimonials-section">
      <h2 class="section-title">What Our Passengers Say</h2>
      <div class="testimonials-carousel">
        <div class="testimonial-card" v-for="(testimonial, index) in testimonials" :key="index">
          <div class="testimonial-content">
            <p class="testimonial-text">"{{ testimonial.text }}"</p>
            <div class="testimonial-author">
              <div class="author-avatar" :style="{ backgroundImage: `url(${testimonial.avatar})` }"></div>
              <div class="author-info">
                <h4>{{ testimonial.name }}</h4>
                <p>{{ testimonial.location }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Newsletter -->
    <section class="newsletter-section">
      <div class="newsletter-content">
        <h2>Stay Updated with Special Offers</h2>
        <p>Subscribe to our newsletter and never miss our promotions</p>
        <div class="newsletter-form">
          <input type="email" placeholder="Your email address" />
          <button>Subscribe</button>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  data() {
    return {
      destinations: [
        {
          name: "Paris, France",
          subtitle: "The City of Light",
          imageUrl: "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?q=80&w=2073&auto=format&fit=crop"
        },
        {
          name: "Tokyo, Japan",
          subtitle: "Where Tradition Meets Innovation",
          imageUrl: "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?q=80&w=1988&auto=format&fit=crop"
        },
        {
          name: "Santorini, Greece",
          subtitle: "Paradise on Earth",
          imageUrl: "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?q=80&w=2069&auto=format&fit=crop"
        },
        {
          name: "New York, USA",
          subtitle: "The City That Never Sleeps",
          imageUrl: "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?q=80&w=2070&auto=format&fit=crop"
        },
        {
          name: "Bali, Indonesia",
          subtitle: "Island of the Gods",
          imageUrl: "https://images.unsplash.com/photo-1537996194471-e657df975ab4?q=80&w=2038&auto=format&fit=crop"
        },
        {
          name: "Dubai, UAE",
          subtitle: "City of Gold",
          imageUrl: "https://images.unsplash.com/photo-1518684079-3c830dcef090?q=80&w=2069&auto=format&fit=crop"
        }
      ],
      features: [
        {
          icon: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
          title: "Competitive Prices",
          description: "Enjoy the best value for your money with our transparent pricing policy."
        },
        {
          icon: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M6.633 10.5c.806 0 1.533-.446 2.031-1.08a9.041 9.041 0 012.861-2.4c.723-.384 1.35-.956 1.653-1.715a4.498 4.498 0 00.322-1.672V3a.75.75 0 01.75-.75A2.25 2.25 0 0116.5 4.5c0 1.152-.26 2.243-.723 3.218-.266.558.107 1.282.725 1.282h3.126c1.026 0 1.945.694 2.054 1.715.045.422.068.85.068 1.285a11.95 11.95 0 01-2.649 7.521c-.388.482-.987.729-1.605.729H13.48c-.483 0-.964-.078-1.423-.23l-3.114-1.04a4.501 4.501 0 00-1.423-.23H5.904M14.25 9h2.25M5.904 18.75c.083.205.173.405.27.602.197.4-.078.898-.523.898h-.908c-.889 0-1.713-.518-1.972-1.368a12 12 0 01-.521-3.507c0-1.553.295-3.036.831-4.398C3.387 10.203 4.167 9.75 5 9.75h1.053c.472 0 .745.556.5.96a8.958 8.958 0 00-1.302 4.665c0 1.194.232 2.333.654 3.375z" /></svg>',
          title: "Premium Comfort",
          description: "Experience luxury and comfort with our modern aircraft fleet."
        },
        {
          icon: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z" /></svg>',
          title: "Flexible Options",
          description: "Choose from a variety of fare options to suit your travel needs."
        },
        {
          icon: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 01-1.043 3.296 3.745 3.745 0 01-3.296 1.043A3.745 3.745 0 0112 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 01-3.296-1.043 3.745 3.745 0 01-1.043-3.296A3.745 3.745 0 013 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 011.043-3.296 3.746 3.746 0 013.296-1.043A3.746 3.746 0 0112 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 013.296 1.043 3.746 3.746 0 011.043 3.296A3.745 3.745 0 0121 12z" /></svg>',
          title: "Reliable Service",
          description: "Count on our punctuality and dedication to customer satisfaction."
        }
      ],
      testimonials: [
        {
          text: "SkySaver Airlines made my trip to Europe amazing! The service was exceptional, and the staff went above and beyond.",
          name: "Sarah Johnson",
          location: "New York, USA",
          avatar: "https://randomuser.me/api/portraits/women/32.jpg"
        },
        {
          text: "Flying with SkySaver has been consistently pleasant. Their prices are competitive, and the comfort level is outstanding.",
          name: "Michael Chen",
          location: "Toronto, Canada",
          avatar: "https://randomuser.me/api/portraits/men/44.jpg"
        },
        {
          text: "I appreciate the punctuality and professionalism of SkySaver. They've become my go-to airline for all my travels.",
          name: "Emma Rodriguez",
          location: "London, UK",
          avatar: "https://randomuser.me/api/portraits/women/63.jpg"
        }
      ]
    };
  }
};
</script>

<style scoped>
.home-container {
  width: 100%;
  overflow-x: hidden;
}

/* Hero Section */
.hero-section {
  height: 80vh;
  background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), 
                    url('https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?q=80&w=2070&auto=format&fit=crop');
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 0 20px;
}

.hero-content {
  max-width: 800px;
  color: white;
}

.main-title {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.subtitle {
  font-size: 1.5rem;
  margin-bottom: 2rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.cta-button {
  display: inline-block;
  background-color: #3b82f6;
  color: white;
  padding: 1rem 2rem;
  border-radius: 0.5rem;
  font-size: 1.25rem;
  font-weight: 600;
  text-decoration: none;
  transition: background-color 0.3s ease;
}

.cta-button:hover {
  background-color: #2563eb;
}

/* Section Styles */
section {
  padding: 5rem 2rem;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 3rem;
  color: #1f2937;
}

/* Featured Destinations */
.destinations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1280px;
  margin: 0 auto;
}

.destination-card {
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.destination-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.2);
}

.destination-image {
  height: 250px;
  background-size: cover;
  background-position: center;
  position: relative;
}

.destination-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);
  padding: 1.5rem;
  color: white;
}

.destination-overlay h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

/* Features Section */
.features-section {
  background-image: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), 
                   url('https://images.unsplash.com/photo-1436491865332-7a61a109cc05?q=80&w=2074&auto=format&fit=crop');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  position: relative;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 2rem;
  max-width: 1280px;
  margin: 0 auto;
}

.feature-card {
  background-color: white;
  padding: 2rem;
  border-radius: 1rem;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-icon {
  width: 4rem;
  height: 4rem;
  margin: 0 auto 1.5rem;
  color: #3b82f6;
}

.feature-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #1f2937;
}

.feature-card p {
  color: #6b7280;
}

/* Testimonials */
.testimonials-carousel {
  display: flex;
  gap: 2rem;
  max-width: 1280px;
  margin: 0 auto;
  overflow-x: auto;
  padding: 1rem 0;
  scrollbar-width: none; /* Firefox */
}

.testimonials-carousel::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Edge */
}

.testimonial-card {
  flex: 0 0 400px;
  background-color: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.testimonial-text {
  font-size: 1.125rem;
  line-height: 1.7;
  margin-bottom: 1.5rem;
  color: #4b5563;
  font-style: italic;
}

.testimonial-author {
  display: flex;
  align-items: center;
}

.author-avatar {
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 50%;
  background-size: cover;
  background-position: center;
  margin-right: 1rem;
}

.author-info h4 {
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.author-info p {
  color: #6b7280;
  font-size: 0.875rem;
}

/* Newsletter Section */
.newsletter-section {
  background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                    url('https://images.unsplash.com/photo-1454496522488-7a8e488e8606?q=80&w=2076&auto=format&fit=crop');
  background-size: cover;
  background-position: center;
  color: white;
  text-align: center;
}

.newsletter-content {
  max-width: 700px;
  margin: 0 auto;
}

.newsletter-content h2 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.newsletter-content p {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.newsletter-form {
  display: flex;
  gap: 0.5rem;
  max-width: 500px;
  margin: 0 auto;
}

.newsletter-form input {
  flex: 1;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem 0 0 0.5rem;
  border: none;
  font-size: 1rem;
}

.newsletter-form button {
  background-color: #3b82f6;
  color: white;
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0 0.5rem 0.5rem 0;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.newsletter-form button:hover {
  background-color: #2563eb;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .main-title {
    font-size: 2.5rem;
  }
  
  .subtitle {
    font-size: 1.25rem;
  }
  
  .features-grid, .destinations-grid {
    grid-template-columns: 1fr;
  }
  
  .newsletter-form {
    flex-direction: column;
  }
  
  .newsletter-form input,
  .newsletter-form button {
    border-radius: 0.5rem;
    width: 100%;
  }
}
</style>