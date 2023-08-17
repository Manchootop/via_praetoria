from shared.functions import delete_main_photo, delete_all_photos, upload_image_product_url, \
    has_difference_images, upload_other_images_product_url
from shared.models import TimeBaseModel
from shared.permissions import IsAdminUserOrReadOnly, IsOwnerOrIsAdminOrReadOnly
from shared.serializers import GetEmailSerializer
from shared.views import CRUDViewSet