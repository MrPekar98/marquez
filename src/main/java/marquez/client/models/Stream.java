/*
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package marquez.client.models;

import static marquez.client.models.DatasetType.STREAM;

import java.time.Instant;
import javax.annotation.Nullable;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NonNull;
import lombok.ToString;

@EqualsAndHashCode(callSuper = true)
@ToString(callSuper = true)
public final class Stream extends Dataset {
  @Getter String schemaLocation;

  public Stream(
      String name,
      String physicalName,
      Instant createdAt,
      Instant updatedAt,
      String sourceName,
      @NonNull String schemaLocation,
      @Nullable String description) {
    super(STREAM, name, physicalName, createdAt, updatedAt, sourceName, description);
    this.schemaLocation = schemaLocation;
  }
}
