import sys
from pathlib import Path

package_dir = Path(__file__).resolve().parent
package_dir_text = str(package_dir)
if package_dir_text not in sys.path:
    sys.path.insert(0, package_dir_text)
