document.addEventListener("DOMContentLoaded", function () {
  const taskList = document.getElementById("taskList");

  // Fonction pour marquer une tâche comme faite
  document.querySelectorAll(".done-button").forEach(button => {
    button.addEventListener("click", function () {
      const taskId = this.dataset.id;

      fetch(`/done/${taskId}`, {
        method: "POST"
      }).then(() => {
        location.reload(); // Recharge la page pour voir l'effet
      });
    });
  });

  // Tri avec SortableJS (assure-toi que SortableJS est inclus dans ton projet)
  if (taskList) {
    const sortable = new Sortable(taskList, {
      animation: 150,
      onEnd: function () {
        const newOrder = [];
        taskList.querySelectorAll(".task").forEach(task => {
          newOrder.push(parseInt(task.dataset.taskId));
        });

        fetch("/update_order", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ order: newOrder }),
        });
      },
    });
  }
  document.getElementById("zoneFilter").addEventListener("change", function () {
    const selectedZone = this.value;
    document.querySelectorAll('#longZone .task').forEach(task => {
        const zone = task.getAttribute('data-zone');
        if (selectedZone === "all" || zone === selectedZone) {
            task.style.display = "block";
        } else {
            task.style.display = "none";
        }
    });
});
document.getElementById("urgentToggle").addEventListener("change", function () {
    const showUrgentOnly = this.checked;

    document.querySelectorAll(".task").forEach(task => {
        const freq = parseFloat(task.getAttribute("data-frequency"));
        const remaining = parseFloat(task.getAttribute("data-remaining"));

        let isUrgent = false;

        if (freq < 30 && remaining <= 35 * 3600) {
            isUrgent = true;
        } else if (freq >= 30 && remaining <= 80 * 3600) {
            isUrgent = true;
        }

        task.style.display = (!showUrgentOnly || isUrgent) ? "block" : "none";
    });
});


});
