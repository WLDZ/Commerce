document.addEventListener('DOMContentLoaded', function () {
    var modal = new bootstrap.Modal(document.getElementById('imageModal'));
    var carousel = new bootstrap.Carousel(document.getElementById('modalCarousel'));

    // Show the modal and carousel on clicking an image
    document.querySelectorAll('.carousel-item img').forEach(function (image, index) {
      image.addEventListener('click', function () {
        modal.show();
        carousel.to(index); // Go to the selected image in the carousel
      });
    });

    // Hide the modal when the carousel is closed
    document.getElementById('imageModal').addEventListener('hidden.bs.modal', function () {
      carousel.pause();
    });
  });