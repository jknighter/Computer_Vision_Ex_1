#pragma once
// glow OpenGL wrapper
#include <glow/common/log.hh>
#include <glow/common/scoped_gl.hh>
#include <glow/objects/ArrayBuffer.hh>
#include <glow/objects/Framebuffer.hh>
#include <glow/objects/Program.hh>
#include <glow/objects/Texture2D.hh>
#include <glow/objects/TextureRectangle.hh>
#include <glow/objects/VertexArray.hh>

// The class GBuffer maintains all the textures rendered in geometry pass of deferred rendering
class GBuffer
{
public:
    enum GBufferType{
        GBUFFER_POSITION,
		GBUFFER_NORMAL
    };

    GBuffer();

    ~GBuffer();

	void init();

    glow::UsedProgram renderToGBuffer();

    void readFromGBuffer(glow::UsedProgram shader);

private:
    glow::SharedFramebuffer mFrameBuffer;
    std::vector<glow::SharedTextureRectangle> mGBuffers;
    glow::SharedProgram mShaderGBuffer;
};