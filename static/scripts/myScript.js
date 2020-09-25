$(document).ready(function () {
  // When clicked, resets the value of the file input and styling
  $("#resetFiles").click(function () {
    $("#fileLoader").val("");
    $(".drop-zone ").removeClass("drop-zone__has_files");
    $(".drop-zone ").removeClass("drop-zone__over");
  });

  // Check for click events on the navbar burger icon
  // From https://bulma.io/documentation/components/navbar/
  $(".navbar-burger").click(function () {
    // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
    $(".navbar-burger").toggleClass("is-active");
    $(".navbar-menu").toggleClass("is-active");
  });

  // Drag and Drop functionality adapted from:
  // https://www.youtube.com/watch?v=Wtrin7C4b7w

  document.querySelectorAll(".drop-zone__input").forEach((inputElement) => {
    const dropZoneElement = inputElement.closest(".drop-zone");

    dropZoneElement.addEventListener("click", (e) => {
      inputElement.click();
    });

    dropZoneElement.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropZoneElement.classList.add("drop-zone__over");
    });

    ["dragleave", "dragend"].forEach((type) => {
      dropZoneElement.addEventListener(type, (e) => {
        dropZoneElement.classList.remove("drop-zone__over");
        $("#submitFiles").prop("disabled", false);
        $("#resetFiles").prop("disabled", false);
      });
    });

    dropZoneElement.addEventListener("drop", (e) => {
      e.preventDefault();
      if (e.dataTransfer.files.length) {
        inputElement.files = e.dataTransfer.files;
      }
    });
  });

  // Checks every 0.001 seconds if any files have been uploaded
  // If 0 files, disables the buttons on the page and does not put the black border on the input area.
  // If >1 files are uploaded, enables the buttons and puts a black order on the input area.
  window.setInterval(function () {
    if ($("#fileLoader").get(0).files.length === 0) {
      $("#submitFiles").prop("disabled", true);
      $("#resetFiles").prop("disabled", true);
      $(".drop-zone ").removeClass("drop-zone__has_files");
    } else {
      $("#submitFiles").prop("disabled", false);
      $("#resetFiles").prop("disabled", false);
      $(".drop-zone ").addClass("drop-zone__has_files");
    }
  }, 1);
});
