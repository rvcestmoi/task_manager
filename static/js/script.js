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
});
