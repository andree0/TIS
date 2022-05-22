from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Species(models.Model):
    # polish_name = models.CharField(max_length=64)
    latin_name = models.CharField(max_length=64)

    class Meta:
        ordering = ["latin_name"]

    def __str__(self):
        return f"{self.latin_name}"  # + f" / {self.polish_name}"


class Inventory(models.Model):
    STATUS_CHOICES = (
        (0, "Inventory"),
        (1, "Valorization"),
        (2, "Tree management"),
    )
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=64)
    created_date = models.DateField(auto_now_add=True)
    edited_date = models.DateField(auto_now=True)
    finish_date = models.DateField(null=True)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=0)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    principal = models.CharField(max_length=64)
    principal_address = models.CharField(max_length=128, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ["id", "author"]

    def __str__(self):
        return f"""{self.pk} - {self.name}"""


class Tree(models.Model):
    ROLOFF_CHOICES = (
        (0, "0"),
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
    )
    lp = models.PositiveIntegerField(default=1)
    species = models.ForeignKey(
        Species,
        on_delete=models.CASCADE,
        help_text="Basic tree species found in Poland.",
    )
    height = models.PositiveIntegerField(
        verbose_name="Height [meters]",
        help_text="Height of tree mansured from base to top of tree.",
    )
    crown_width = models.PositiveIntegerField(
        verbose_name="Crown width [meters]",
        help_text="Tree crown width measured at its widest point.",
    )
    roloff = models.PositiveSmallIntegerField(
        choices=ROLOFF_CHOICES,
        default=0,
        help_text="Crown structure and tree vitality in Roloff scale.",
    )
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    is_existing = models.BooleanField(default=True)

    class Meta:
        unique_together = ["lp", "inventory"]

    def __str__(self):
        return f"""I{self.inventory.id} / T{self.lp}"""


class ValorizationTree(models.Model):
    VALUE_CHOICES = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )
    tree = models.OneToOneField("Tree", on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(choices=VALUE_CHOICES, default=5)
    is_biocenotic = models.BooleanField(
        default=False,
    )


class ManagementTree(models.Model):
    PROCEDURE_CHOICES = (
        (0, "ok"),
        (1, "intervention"),
        (2, "removal"),
    )
    tree = models.OneToOneField("Tree", on_delete=models.CASCADE)
    procedure = models.PositiveSmallIntegerField(
        choices=PROCEDURE_CHOICES,
        default=0,
    )


class Circuit(models.Model):
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    value = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(600)],
        verbose_name="Circuit",
        help_text="Circuit of a single trunk at a height of DBH \
            (breast height diameter).",
    )

    def __str__(self) -> str:
        return f"""{self.tree} - {self.value}"""


class Photo(models.Model):
    image = models.ImageField(upload_to="tree_photos")
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)


class TreeComment(models.Model):
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    description = models.TextField()
    created = models.DateTimeField(auto_now=True)
